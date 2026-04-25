"""
Improved DOCX parser v5.
Fixes:
1. Tin học: missing 'A.' (Emphasis)
2. Tin học: "dãy số A." false split
3. English: Passage repetition in sub-questions
4. English: Better choice/question separation in reading sections
5. English: Phonetics split correctly
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

# ─── Helpers ──────────────────────────────────────────────────────────────────

def get_paras(filepath):
    doc = Document(filepath)
    result = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            result.append(None)
        else:
            # Capture bold text properly
            bold_text = "".join(r.text for r in para.runs if r.bold).strip()
            result.append({'text': text, 'bold': bold_text})
    return result

def is_question_start(text):
    # Matches 'Câu 1:', 'Question 1.', '1.', '31.' etc.
    return bool(re.match(r'^(?:Câu|Question|Q|(\d+))\s*\d*[\.\:\)]\s*', text, re.I))

def get_choice_marker(text):
    # Returns 'A', 'B', 'C', or 'D' if line starts with it
    m = re.match(r'^([A-D])[\.\)]\s*', text)
    return m.group(1) if m else None

def has_embedded_choices(text):
    # Check if a line has multiple choice markers like 'A. ... B. ...'
    return len(re.findall(r'(?<!\w)[A-D][\.\)]\s+', text)) >= 1

def clean_text(text):
    return text.replace('\xa0', ' ').replace('\t', ' ').strip()

def split_choices(text, bold_text):
    # Split a line into choices, handling missing 'A.'
    text = text.replace('\xa0', ' ').strip()
    
    # If it has B. but no A. at start, prepend A.
    if not re.match(r'^[A-D][\.\)]', text) and re.search(r'(?<!\w)B[\.\)]\s+', text):
        text = "A. " + text
        
    # Split using markers
    parts = re.split(r'(?<!\w)([A-D][\.\)]\s+)', text)
    res = []
    i = 1
    if len(parts) == 1:
        res.append(parts[0])
    else:
        while i < len(parts):
            marker = parts[i].strip()
            content = parts[i+1].strip() if i+1 < len(parts) else ""
            res.append(f"{marker} {content}")
            i += 2
            
    # Fallback for tab-split
    if len(res) < 2 and '\t' in text:
        tab_parts = [p.strip() for p in text.split('\t') if p.strip()]
        if len(tab_parts) >= 2:
            res = []
            for idx, p in enumerate(tab_parts[:4]):
                p_clean = re.sub(r'^[A-D][\.\)]\s*', '', p)
                res.append(f"{chr(65+idx)}. {p_clean}")

    # Find answer
    answer = -1
    if bold_text and res:
        b_clean = re.sub(r'^[A-D][\.\)]\s*', '', bold_text).strip()
        for idx, c in enumerate(res):
            c_clean = re.sub(r'^[A-D][\.\)]\s*', '', c).strip()
            if b_clean and (b_clean in c_clean or c_clean in b_clean) and len(b_clean) > 1:
                answer = idx
                break
    return res, answer

def parse_subject(paras, topic_id, is_english=False):
    problems = []
    instruction = ""
    passage = []
    
    curr_q = []
    curr_choices = []
    curr_ans = -1
    
    def save():
        nonlocal curr_q, curr_choices, curr_ans
        if not curr_q and not curr_choices: return
        
        q_text = "\n".join(curr_q).strip()
        # If we have a passage, prepend it
        full_q = []
        if instruction: full_q.append(instruction)
        if passage: full_q.append("\n".join(passage))
        if q_text: full_q.append(q_text)
        
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
        
        # Instruction / Header detection
        if text.isupper() and len(text) < 100:
            save()
            instruction = text
            passage = []
            continue
            
        if re.match(r'^(Choose|Read the following|Mark the|Hãy chọn|Chọn)', text, re.I):
            save()
            instruction = text
            passage = []
            continue

        # Question Start
        if is_question_start(text):
            save()
            # Check for embedded choices
            if has_embedded_choices(text):
                # Try to separate question from choices
                # Look for the first A. or B.
                m = re.search(r'(?<!\w)[A-D][\.\)]\s+', text)
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
        marker = get_choice_marker(text)
        if marker or has_embedded_choices(text):
            choices, ans = split_choices(text, bold)
            if marker == 'A' or (not curr_choices and marker is None):
                # New set of choices
                if curr_choices: save()
                curr_choices = choices
                curr_ans = ans
            else:
                # Continuation
                curr_choices.extend(choices)
                if ans != -1: curr_ans = len(curr_choices) - len(choices) + ans
            
            if len(curr_choices) >= 4: save()
            continue
            
        # Accumulation
        if instruction and "Read the following" in instruction and not curr_q:
            passage.append(text)
        elif curr_choices:
            # Plain text after choices? Probably next question or essay
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
    
    # Load current data
    prob_path = r"E:\toanvui-main\src\data\problems.js"
    with open(prob_path, encoding="utf-8") as f:
        all_probs = json.loads(f.read().replace("export const problems = ", "").rstrip(";\n "))
        
    topic_path = r"E:\toanvui-main\src\data\topics.js"
    with open(topic_path, encoding="utf-8") as f:
        all_topics = json.loads(f.read().replace("export const topics = ", "").rstrip(";\n "))

    for s in SUBJECTS:
        print(f"Parsing {s['id']}...")
        paras = get_paras(s['file'])
        new_probs = parse_subject(paras, s['id'], is_english=(s['id'] == 'g7-english'))
        print(f"  Found {len(new_probs)} problems.")
        
        # Remove old
        for k in list(all_probs.keys()):
            if k.startswith(s['id'] + "-"): del all_probs[k]
            
        # Add new
        for p in new_probs:
            all_probs[p['id']] = p
            
        # Update topics
        for g in all_topics.get('7', []):
            if g['id'] == s['id']:
                g['problemIds'] = [p['id'] for p in new_probs]
                break

    # Save
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
