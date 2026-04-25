"""
Improved DOCX parser v11 with logging and better state clearing.
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
    # Marker must be at start or preceded by any whitespace
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
        curr_q = []
        curr_choices = []
        curr_ans = -1

    for p in paras:
        if p is None:
            if curr_choices: save()
            continue
            
        text = p['text']
        bold = p['bold']
        
        # Section Header (all caps, short)
        if text.isupper() and len(text) < 100:
            save()
            instruction = text
            passage = []
            in_reading = False
            continue
            
        # Reading/Passage Instruction (strict)
        if re.match(r'^(Read the following|Đoạn văn)', text, re.I):
            save()
            instruction = text
            passage = []
            in_reading = True
            continue
            
        # General Instruction (not reading)
        if re.match(r'^(Choose|Mark the|Hãy chọn|Chọn)', text, re.I):
            save()
            instruction = text
            passage = [] # Clear passage for new general section
            in_reading = False
            continue

        # New Question detection
        if is_question_start(text):
            save()
            # If not in a reading section, clear old passage/instruction
            if not in_reading:
                passage = []
                # instruction = "" # Keep instruction for non-reading sections usually

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
            
        # Choice line detection
        if has_choice_marker(text):
            choices, ans = split_into_choices(text, bold)
            # Start new set if A. or we have nothing yet
            if re.match(r'^A[\.\)]', text) or not curr_choices:
                if curr_choices: save()
                curr_choices = choices
                curr_ans = ans
            else:
                curr_choices.extend(choices)
                if ans != -1: curr_ans = len(curr_choices) - len(choices) + ans
            
            if len(curr_choices) >= 4: save()
            continue
            
        # Accumulation
        if in_reading and not curr_q:
            passage.append(text)
        elif curr_choices:
            save()
            curr_q = [text]
        else:
            curr_q.append(text)
            
    save()
    return problems

def run():
    SUBJECTS = [
        {"file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx", "id": "g7-tin"},
        {"file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx", "id": "g7-english"},
    ]
    prob_path = r"E:\toanvui-main\src\data\problems.js"
    topic_path = r"E:\toanvui-main\src\data\topics.js"
    
    with open(prob_path, encoding="utf-8") as f:
        all_probs = json.loads(f.read().replace("export const problems = ", "").rstrip(";\n "))
    with open(topic_path, encoding="utf-8") as f:
        all_topics = json.loads(f.read().replace("export const topics = ", "").rstrip(";\n "))

    for s in SUBJECTS:
        print(f"Parsing {s['id']}...")
        paras = get_paras(s['file'])
        new_probs = parse_docx(paras, s['id'])
        print(f"  Found {len(new_probs)} problems.")
        for k in list(all_probs.keys()):
            if k.startswith(s['id'] + "-"): del all_probs[k]
        for p in new_probs: all_probs[p['id']] = p
        for g in all_topics.get('7', []):
            if g['id'] == s['id']:
                g['problemIds'] = [p['id'] for p in new_probs]
                break

    with open(prob_path, "w", encoding="utf-8") as f:
        f.write("export const problems = ")
        json.dump(all_probs, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    with open(topic_path, "w", encoding="utf-8") as f:
        f.write("export const topics = ")
        json.dump(all_topics, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("Done!")

if __name__ == "__main__":
    run()
