"""
Improved DOCX parser v9.
Final refinements:
1. Marker regex: (?:^|\\t|[ ]{2,})[A-D][\\.\\)]
2. Question regex: ^(?:Câu|Question|Q)\\s*\\d+[\\.\\:\\)]
3. Reading comprehension: Proper passage capture and repetition.
4. Choice splitting: Handle tab and multiple spaces.
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
    # Matches 'Câu 1:', 'Question 1.' but NOT '1.' to avoid false matches with list items
    return bool(re.match(r'^(?:Câu|Question|Q)\s*\d+[\.\:\)]\s*', text, re.I))

def has_any_marker(text):
    # Marker at start, or after tab, or after 2+ spaces
    return bool(re.search(r'(?:^|\t|[ ]{2,})[A-D][\.\)]', text))

def split_choices(text, bold_text):
    text = text.replace('\xa0', ' ').strip()
    
    # Prepend A. if missing but B. exists later (e.g. Emphasis \tB. ...)
    if not re.match(r'^[A-D][\.\)]', text) and re.search(r'(?:\t|[ ]{2,})B[\.\)]', text):
        text = "A. " + text
        
    # Split by markers
    # We find all matches of markers
    markers = list(re.finditer(r'(?:^|\t|[ ]{2,})([A-D][\.\)])', text))
    res = []
    if not markers:
        res.append(text)
    else:
        for i in range(len(markers)):
            start = markers[i].start(1) # Start of the [A-D][. )] part
            end = markers[i+1].start(1) if i+1 < len(markers) else len(text)
            segment = text[start:end].strip()
            if segment: res.append(segment)
            
    # Fallback for tab-split if no markers found but looks like 4 options
    if len(res) < 2 and '\t' in text:
        tab_parts = [p.strip() for p in text.split('\t') if p.strip()]
        if len(tab_parts) >= 2:
            res = [f"{chr(65+j)}. {p}" for j, p in enumerate(tab_parts[:4])]

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
    
    in_reading_mode = False
    
    def save():
        nonlocal curr_q, curr_choices, curr_ans
        if not curr_q and not curr_choices: return
        
        q_lines = [q for q in curr_q if q.strip()]
        if not q_lines and not curr_choices: return

        # Build full question
        full_q_parts = []
        if instruction: full_q_parts.append(instruction)
        if in_reading_mode and passage: full_q_parts.append("\n".join(passage))
        if q_lines: full_q_parts.append("\n".join(q_lines))
        
        q_final = "\n".join(full_q_parts).replace('\t', ' _____ ').strip()
        
        # Format choices
        final_choices = []
        for idx, c in enumerate(curr_choices[:4]):
            prefix = f"{chr(65+idx)}. "
            c_clean = re.sub(r'^[A-D][\.\)]\s*', '', c).strip()
            final_choices.append(f"{prefix}{c_clean}")
            
        problems.append({
            "id": f"{topic_id}-{len(problems)+1}",
            "topicId": topic_id,
            "question": q_final,
            "choices": final_choices,
            "answer": curr_ans,
            "type": "multiple-choice" if final_choices else "essay",
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
        
        # Header detection
        if text.isupper() and len(text) < 100:
            save()
            instruction = text
            passage = []
            in_reading_mode = False
            continue
            
        # Instruction detection
        if re.match(r'^(Choose|Read the following|Mark the|Hãy chọn|Chọn)', text, re.I):
            save()
            instruction = text
            passage = []
            in_reading_mode = 'Read the following' in text or 'reading' in text.lower() or 'đoạn văn' in text.lower()
            continue

        # New Question detection
        if is_question_start(text):
            save()
            # If line has markers, it's a self-contained Q+A line
            if has_any_marker(text):
                m = re.search(r'(?:^|\t|[ ]{2,})[A-D][\.\)]', text)
                q_part = text[:m.start()].strip()
                c_part = text[m.start():].strip()
                curr_q = [q_part] if q_part else []
                curr_choices, curr_ans = split_choices(c_part, bold)
                save()
                continue
            curr_q = [text]
            continue
            
        # Choice line detection
        if has_any_marker(text):
            choices, ans = split_choices(text, bold)
            # Starts with A. or we have no choices yet -> new set
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
        if in_reading_mode and not curr_q:
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
    with open(prob_path, encoding="utf-8") as f:
        all_probs = json.loads(f.read().replace("export const problems = ", "").rstrip(";\n "))
    topic_path = r"E:\toanvui-main\src\data\topics.js"
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
