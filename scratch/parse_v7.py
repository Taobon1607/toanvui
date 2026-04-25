"""
Improved DOCX parser v7.
Fixes:
1. Regex for markers: Use (?<=\s|^) to avoid splitting 'dãy A.'
2. Tin học: Emphasis handled via split_choices prepending A.
3. English Reading: Prepend passage to each sub-question.
4. Clean up question accumulation to avoid leaking old choice lines.
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

def has_any_marker(text):
    # Marker must be at start or preceded by space
    return bool(re.search(r'(?<=\s|^)[A-D][\.\)]\s*', text))

def split_choices(text, bold_text):
    text = text.replace('\xa0', ' ').strip()
    
    # Prepend A. if missing but B. exists later
    if not re.match(r'^[A-D][\.\)]', text) and re.search(r'(?<=\s|^)B[\.\)]\s*', text):
        text = "A. " + text
        
    # Split by markers
    parts = re.split(r'(?<=\s|^)([A-D][\.\)]\s*)', text)
    res = []
    if len(parts) == 1:
        res.append(parts[0].strip())
    else:
        # parts[0] is empty if string starts with marker
        if parts[0].strip():
            res.append(parts[0].strip())
        i = 1
        while i < len(parts):
            marker = parts[i].strip()
            content = parts[i+1].strip() if i+1 < len(parts) else ""
            res.append(f"{marker} {content}")
            i += 2
            
    # Fallback for tab-split (e.g. phonetics)
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

        # Build question text
        full_q = []
        if instruction: full_q.append(instruction)
        if in_reading_mode and passage: full_q.append("\n".join(passage))
        if q_lines: full_q.append("\n".join(q_lines))
        
        q_final = "\n".join(full_q).replace('\t', ' _____ ').strip()
        
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
        
        # Header/Instruction detect
        if text.isupper() and len(text) < 100:
            save()
            instruction = text
            passage = []
            in_reading_mode = False
            continue
        if re.match(r'^(Choose|Read the following|Mark the|Hãy chọn|Chọn)', text, re.I):
            save()
            instruction = text
            passage = []
            in_reading_mode = 'Read the following' in text or 'reading' in text.lower() or 'đoạn văn' in text.lower()
            continue

        # Question Start
        if is_question_start(text):
            save()
            if has_any_marker(text):
                # Embedded choices
                m = re.search(r'(?<=\s|^)[A-D][\.\)]\s*', text)
                if m:
                    q_part = text[:m.start()].strip()
                    c_part = text[m.start():].strip()
                    curr_q = [q_part]
                    curr_choices, curr_ans = split_choices(c_part, bold)
                    save()
                    continue
            curr_q = [text]
            continue
            
        # Choice detection
        if has_any_marker(text):
            choices, ans = split_choices(text, bold)
            # If starts with A. or no choices yet, it's a new set
            if re.match(r'^[A][\.\)]', text) or not curr_choices:
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
