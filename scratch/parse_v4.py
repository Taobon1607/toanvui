"""
Improved DOCX parser v4.
Fixes:
1. Tin học: Missing "A." prefix (e.g. Emphasis).
2. Tin học: "dãy số A." false split (regex fix).
3. Tiếng Anh: Repeat passage for each sub-question.
4. Tiếng Anh: Phonetics/Stress better splitting.
5. Robust choice prefixing (A, B, C, D) when missing.
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
            bold_text = "".join(r.text for r in para.runs if r.bold).strip()
            result.append((text, bold_text))
    return result


def is_question_start(text):
    """True if paragraph begins a new question (e.g., 'Câu 1:', 'Question 1.', '1.')"""
    return bool(re.match(
        r'^(Câu\s*\d+[\:\.)]|Question\s*\d+[\:\.)]|\d+[\.\)]\s+\S)',
        text, re.I
    ))


def starts_with_choice(text):
    """True if text begins with A. B. C. D. or A) B) C) D)"""
    return bool(re.match(r'^[A-D][\.\)]\s*', text))


def has_any_choice_marker(text):
    """True if text contains any A. B. C. D. markers."""
    return bool(re.search(r'(?<!\w)[A-D][\.\)]\s+', text))


def split_choices_line(text, bold_text):
    """
    Split a single-line containing multiple choices.
    Handles missing 'A.' at the start.
    """
    text = text.replace('\xa0', ' ').strip()
    
    # Check if it starts with a choice marker. If not, but it has a 'B.', prepend 'A.'
    if not starts_with_choice(text) and re.search(r'(?<!\w)B[\.\)]\s+', text):
        text = "A. " + text

    # Split on markers followed by space. Avoid splitting 'dãy A.' at end of string.
    # We use a lookahead for a space or end of string.
    parts = re.split(r'(?<!\w)([A-D][\.\)]\s+)', text)
    
    choices = []
    i = 1
    # parts[0] is text before first marker
    if parts[0].strip() and not i < len(parts):
        # Only one part, no markers found
        choices.append(parts[0].strip())
    
    while i < len(parts) - 1:
        letter = parts[i].strip()
        content = parts[i + 1].strip()
        choices.append(f"{letter} {content}")
        i += 2
    
    # Fallback for tab-separated without markers
    if not choices and '\t' in text:
        raw = [p.strip() for p in text.split('\t') if p.strip()]
        for idx, p in enumerate(raw[:4]):
            prefix = ["A. ", "B. ", "C. ", "D. "][idx]
            if not re.match(r'^[A-D][\.\)]', p):
                p = prefix + p
            choices.append(p)
            
    if not choices:
        choices.append(text)

    # Determine correct answer
    answer = -1
    if bold_text and choices:
        clean_bold = re.sub(r'^[A-D][\.\)]\s*', '', bold_text).replace('\xa0', ' ').strip()
        for idx, c in enumerate(choices):
            clean_c = re.sub(r'^[A-D][\.\)]\s*', '', c).replace('\xa0', ' ').strip()
            if clean_bold and (clean_bold in clean_c or clean_c in clean_bold) and len(clean_bold) > 1:
                answer = idx
                break
    return choices, answer


def make_problem(topicId, counter, q_lines, choices, answer, instruction=None, passage=None):
    counter[0] += 1
    
    final_q_parts = []
    if instruction:
        final_q_parts.append("\n".join(instruction))
    if passage:
        final_q_parts.append("\n".join(passage))
    if q_lines:
        final_q_parts.append("\n".join(q_lines))
        
    q_text = "\n".join(final_q_parts).strip()
    q_text = q_text.replace('\t', ' _____ ').replace('\xa0', ' ')
    
    # Ensure all choices have A. B. C. D.
    final_choices = []
    for idx, c in enumerate(choices):
        prefix = ["A. ", "B. ", "C. ", "D. "][idx] if idx < 4 else ""
        if not re.match(r'^[A-D][\.\)]', c):
            c = prefix + c
        final_choices.append(c.replace('\xa0', ' ').replace('\t', ' ').strip())
        
    return {
        "id": f"{topicId}-{counter[0]}",
        "topicId": topicId,
        "question": q_text,
        "choices": final_choices,
        "answer": answer,
        "type": "multiple-choice" if final_choices else "essay",
        "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
    }


# ─── Parsers ──────────────────────────────────────────────────────────────────

def parse_docx(paras, topicId, is_english=False):
    problems = []
    counter = [0]
    
    current_q = []
    current_choices = []
    current_answer = -1
    
    instruction = []
    passage = []
    in_reading = False
    
    def save():
        nonlocal current_q, current_choices, current_answer
        if current_q or current_choices:
            problems.append(make_problem(topicId, counter, current_q, current_choices, current_answer, instruction, passage if in_reading else None))
        current_q.clear()
        current_choices.clear()
        current_answer = -1

    for para in paras:
        if para is None:
            if current_choices:
                save()
            continue
            
        text, bold = para
        
        # Section Header
        if text.isupper() and len(text) < 100 and not starts_with_choice(text):
            save()
            instruction = [text]
            passage = []
            in_reading = False
            continue
            
        # Instruction
        if re.match(r'^(Choose the|Read the following|Mark the letter|Hãy chọn|Chọn đáp án)', text, re.I):
            save()
            instruction = [text]
            passage = []
            in_reading = 'Read the following' in text or 'reading' in text.lower() or 'đoạn văn' in text.lower()
            continue

        # New Question
        if is_question_start(text):
            save()
            # Embedded choices?
            if has_any_choice_marker(text):
                m = re.search(r'(?<!\w)[A-D][\.\)]\s+', text)
                if m:
                    q_part = text[:m.start()].strip()
                    c_part = text[m.start():]
                    current_q = [q_part]
                    current_choices, current_answer = split_choices_line(c_part, bold)
                    save()
                    continue
            current_q = [text]
            continue
            
        # Choice Line
        if has_any_choice_marker(text) or (current_q and starts_with_choice(text)):
            choices, answer = split_choices_line(text, bold)
            
            # If we already have choices and this line starts with A., it might be a new question
            # or it's a phonetics line.
            if is_english and not current_q and not passage:
                # Phonetics: each choice line is a question
                problems.append(make_problem(topicId, counter, [], choices, answer, instruction, None))
                continue

            if current_choices and starts_with_choice(text) and text.strip().startswith('A.'):
                save()
                current_choices = choices
                current_answer = answer
            else:
                current_choices.extend(choices)
                if answer != -1:
                    current_answer = len(current_choices) - len(choices) + answer
            
            if len(current_choices) >= 4:
                save()
            continue

        # Accumulation
        if in_reading and not current_q:
            passage.append(text)
        elif current_choices:
            save()
            current_q = [text]
        else:
            current_q.append(text)
            
    save()
    return problems


# ─── Main ─────────────────────────────────────────────────────────────────────

SUBJECTS = [
    {"file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx", "topicId": "g7-tin"},
    {"file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx", "topicId": "g7-english"},
]

def run():
    problems_path = r"E:\toanvui-main\src\data\problems.js"
    topics_path = r"E:\toanvui-main\src\data\topics.js"

    with open(problems_path, encoding="utf-8") as f:
        prob_dict = json.loads(f.read().replace("export const problems = ", "").rstrip(";\n "))
    with open(topics_path, encoding="utf-8") as f:
        top_dict = json.loads(f.read().replace("export const topics = ", "").rstrip(";\n "))

    for subj in SUBJECTS:
        tid = subj["topicId"]
        print(f"--- {tid} ---")
        paras = get_paras(subj["file"])
        new_probs = parse_docx(paras, tid, is_english=(tid == "g7-english"))
        
        print(f"  Parsed {len(new_probs)} problems")
        
        # Remove old
        old = [k for k in prob_dict if k.startswith(tid + "-")]
        for k in old: del prob_dict[k]
        
        # Add new
        for p in new_probs:
            prob_dict[p["id"]] = p
            
        # Update topics
        for topic in top_dict.get('7', []):
            if topic['id'] == tid:
                topic['problemIds'] = [p['id'] for p in new_probs]
                break

    with open(problems_path, "w", encoding="utf-8") as f:
        f.write("export const problems = ")
        json.dump(prob_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    with open(topics_path, "w", encoding="utf-8") as f:
        f.write("export const topics = ")
        json.dump(top_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("Done.")

if __name__ == "__main__":
    run()
