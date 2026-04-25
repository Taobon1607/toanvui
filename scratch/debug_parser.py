"""
Debug Parser.
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

def get_paras(filepath):
    doc = Document(filepath)
    result = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            result.append(None)
        else:
            bold_text = "".join(r.text for r in para.runs if r.bold).strip()
            result.append({'text': text, 'bold': bold_text})
    return result

def is_question_start(text):
    return bool(re.match(r'^(?:Câu|Question|Q|(\d+))\s*\d*[\.\:\)]\s*', text, re.I))

def has_choice_marker(text):
    return bool(re.search(r'(?:^|\s)[A-D][\.\)]', text))

def split_into_choices(text, bold_text):
    text = text.replace('\xa0', ' ').strip()
    if not re.match(r'^[A-D][\.\)]', text) and re.search(r'(?:^|\s)B[\.\)]', text):
        text = "A. " + text
    markers = list(re.finditer(r'(?:^|\s)([A-D][\.\)])', text))
    res = []
    if not markers:
        res.append(text)
    else:
        for i in range(len(markers)):
            start = markers[i].start(1)
            end = markers[i+1].start(1) if i+1 < len(markers) else len(text)
            seg = text[start:end].strip()
            if seg: res.append(seg)
    answer = -1
    if bold_text and res:
        b_clean = re.sub(r'^[A-D][\.\)]\s*', '', bold_text).strip()
        for idx, c in enumerate(res):
            c_clean = re.sub(r'^[A-D][\.\)]\s*', '', c).strip()
            if b_clean and (b_clean == c_clean or b_clean in c_clean or c_clean in b_clean) and len(b_clean) > 1:
                answer = idx
                break
    return res, answer

def parse_docx(paras, topic_id):
    problems = []
    instruction = ""
    passage = []
    curr_q = []
    curr_choices = []
    curr_ans = -1
    in_reading = False
    
    def save():
        nonlocal curr_q, curr_choices, curr_ans
        if not curr_q and not curr_choices: return
        q_lines = [q for q in curr_q if q.strip()]
        if not q_lines and not curr_choices: return
        full_q = []
        if instruction: full_q.append(instruction)
        if in_reading and passage: full_q.append("\n".join(passage))
        if q_lines: full_q.append("\n".join(q_lines))
        q_text = "\n".join(full_q).replace('\t', ' _____ ').strip()
        formatted_choices = []
        for i, c in enumerate(curr_choices[:4]):
            prefix = f"{chr(65+i)}. "
            clean = re.sub(r'^[A-D][\.\)]\s*', '', c).strip()
            formatted_choices.append(f"{prefix}{clean}")
        problems.append({
            "id": f"{topic_id}-{len(problems)+1}",
            "topicId": topic_id,
            "question": q_text,
            "choices": formatted_choices,
            "answer": curr_ans,
            "type": "multiple-choice" if formatted_choices else "essay",
            "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
        })
        print(f"DEBUG: Saved {topic_id}-{len(problems)} Q:[{q_text[:30]}...] C:{len(formatted_choices)}")
        curr_q = []
        curr_choices = []
        curr_ans = -1

    for i, p in enumerate(paras):
        if p is None:
            if curr_choices: save()
            continue
        text = p['text']
        bold = p['bold']
        print(f"[{i}] {text[:50]} (has_marker:{has_choice_marker(text)}, is_q:{is_question_start(text)})")
        
        if text.isupper() and len(text) < 100:
            save(); instruction = text; passage = []; in_reading = False; continue
        if re.match(r'^(Read the following|Đoạn văn)', text, re.I):
            save(); instruction = text; passage = []; in_reading = True; continue
        if re.match(r'^(Choose|Mark the|Hãy chọn|Chọn)', text, re.I):
            save(); instruction = text; passage = []; in_reading = False; continue

        if is_question_start(text):
            save()
            if not in_reading: passage = []
            if has_choice_marker(text):
                m = re.search(r'(?:^|\s)[A-D][\.\)]', text)
                q_part = text[:m.start()].strip()
                c_part = text[m.start():].strip()
                curr_q = [q_part] if q_part else []
                curr_choices, curr_ans = split_into_choices(c_part, bold)
                save()
                continue
            curr_q = [text]
            continue
            
        if has_choice_marker(text):
            choices, ans = split_into_choices(text, bold)
            if re.match(r'^A[\.\)]', text) or not curr_choices:
                if curr_choices: save()
                curr_choices = choices; curr_ans = ans
            else:
                curr_choices.extend(choices)
                if ans != -1: curr_ans = len(curr_choices) - len(choices) + ans
            if len(curr_choices) >= 4: save()
            continue
            
        if in_reading and not curr_q: passage.append(text)
        elif curr_choices: save(); curr_q = [text]
        else: curr_q.append(text)
            
    save()
    return problems

paras = get_paras(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx")
new_probs = parse_docx(paras[:20], "g7-tin")
