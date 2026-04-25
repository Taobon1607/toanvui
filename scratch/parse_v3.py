"""
Improved DOCX parser v3 - paragraph-by-paragraph approach.
Handles:
  1. Tin học: câu 50 missing "A." prefix, câu 22 "dãy số A" false split
  2. Tiếng Anh: phonetics/stress (multiple questions per section), 
     reading comprehension (passage + sub-questions)

Key rules:
  - Each BLANK line may separate question from choices, or two separate questions
  - A choice line is one that starts with [A-D]. OR is a tab-separated line in a known choices context
  - For phonetics/stress: each tab-separated ABCD line = one question
  - split_choices_line only splits on [A-D]. preceded by tab OR start of string
  - Missing "A." prefix on first item: auto-add
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
    """True if paragraph begins a new question."""
    return bool(re.match(
        r'^(Câu\s*\d+[\:\.)]|Question\s*\d+[\:\.)]|\d+[\.\)]\s+\S)',
        text, re.I
    ))


def starts_with_choice(text):
    """True if text begins with A. B. C. D."""
    return bool(re.match(r'^[A-D][\.\)]\s*\S', text))


def is_all_choices_line(text):
    """True if text is a tab-separated line containing A/B/C/D options (all on one line)."""
    # Must have at least 2 of A/B/C/D markers
    found = re.findall(r'(?:^|\t)\s*[A-D][\.\)]\s*\S', text)
    return len(found) >= 2


def split_choices_line(text, bold_text):
    """
    Split a single-line containing multiple choices by TAB first,
    then by [A-D]. at the start of each segment.
    Returns (choices_list, answer_index).
    """
    # Priority: split by tab
    raw_parts = [p.strip() for p in text.split('\t') if p.strip()]
    
    choices = []
    prefix_letters = ["A. ", "B. ", "C. ", "D. "]
    
    for p in raw_parts:
        p = p.replace('\xa0', ' ').strip()
        if not p:
            continue
        # If this part doesn't start with A./B./C./D., add prefix
        if not re.match(r'^[A-D][\.\)]', p):
            idx = len(choices)
            if idx < 4:
                p = prefix_letters[idx] + p
        choices.append(p)
    
    # Determine correct answer from bold
    answer = -1
    if bold_text and choices:
        clean_bold = re.sub(r'^[A-D][\.\)]\s*', '', bold_text).replace('\xa0', ' ').strip()
        for idx, c in enumerate(choices):
            clean_c = re.sub(r'^[A-D][\.\)]\s*', '', c).replace('\xa0', ' ').strip()
            # Meaningful overlap
            if clean_bold and len(clean_bold) > 1:
                if clean_bold[:12] in clean_c or clean_c[:12] in clean_bold:
                    answer = idx
                    break

    return choices, answer


def make_problem(topicId, counter, q_lines, choices, answer):
    counter[0] += 1
    q_text = "\n".join(q_lines).strip()
    q_text = q_text.replace('\t', ' _____ ').replace('\xa0', ' ')
    cleaned = [c.replace('\xa0', ' ').replace('\t', ' ').strip() for c in choices]
    return {
        "id": f"{topicId}-{counter[0]}",
        "topicId": topicId,
        "question": q_text,
        "choices": cleaned,
        "answer": answer,
        "type": "multiple-choice" if cleaned else "essay",
        "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
    }


# ─── Tin học parser ───────────────────────────────────────────────────────────

def parse_tin(paras, topicId):
    """
    Tin học: each paragraph is either a question or a choice line.
    Question starts with 'Câu X:'.
    Choice line may have A./B./C./D. all on one line (tab-separated)
    OR each choice on its own line.
    """
    problems = []
    counter = [0]
    
    current_q = []
    current_choices = []
    current_answer = -1
    
    def save():
        nonlocal current_q, current_choices, current_answer
        if current_q:
            problems.append(make_problem(topicId, counter, current_q, current_choices, current_answer))
        current_q.clear()
        current_choices.clear()
        current_answer = -1
    
    for para in paras:
        if para is None:
            # blank line: if we have choices, the question is complete
            if current_choices:
                save()
            continue
        
        text, bold = para
        
        # New question
        if is_question_start(text):
            save()
            # Check if choices are embedded in same line
            if is_all_choices_line(text):
                m = re.search(r'(?:^|\t)\s*[A-D][\.\)]', text)
                if m:
                    q_part = text[:m.start()].strip()
                    choices_part = text[m.start():]
                    current_q.append(q_part)
                    current_choices, current_answer = split_choices_line(choices_part, bold)
                    save()
                    continue
            current_q.append(text)
            continue
        
        # All-choices line (tab-separated A./B./C./D. or just A. B. split)
        if is_all_choices_line(text) or starts_with_choice(text):
            choices, answer = split_choices_line(text, bold)
            # If current_choices already exists, it means next set of choices = continuation
            if current_choices and starts_with_choice(text) and text.strip().startswith('C.'):
                # Continuation: C. D. part of same question
                current_choices.extend(choices)
                if answer != -1:
                    current_answer = len(current_choices) - len(choices) + answer
            else:
                current_choices.extend(choices)
                if answer != -1:
                    current_answer = len(current_choices) - len(choices) + answer
            # If we now have 4 choices, question is complete
            if len(current_choices) >= 4:
                save()
            continue
        
        # Plain text: continuation of question or context
        if current_choices:
            # After choices started: some context line, save old and start new
            save()
        current_q.append(text)
    
    save()
    return problems


# ─── Tiếng Anh parser ─────────────────────────────────────────────────────────

def parse_english(paras, topicId):
    """
    Tiếng Anh: paragraph-by-paragraph.
    - Section headers: PHONETICS, GRAMMAR, etc. → set instruction context
    - Instruction lines: 'Choose the word...' → set instruction for next N questions
    - Choice line (all ABCD on one line, tab-separated) → ONE question with current instruction
    - Numbered questions: 'Question X.' or 'Câu X.' → new question
    - Passage text: accumulate as context
    - Reading comprehension: passage text stored, each 'Question X.' sub-problem
      inherits passage as prefix of its question
    """
    problems = []
    counter = [0]
    
    instruction = []   # e.g. ['Choose the word whose underlined part...']
    passage = []       # accumulated reading passage lines
    current_q = []
    current_choices = []
    current_answer = -1
    in_reading = False  # are we inside a reading comprehension passage?
    
    def save(q_override=None):
        nonlocal current_q, current_choices, current_answer
        q_lines = current_q if q_override is None else q_override
        if not q_lines and not current_choices:
            current_q.clear()
            current_choices.clear()
            current_answer = -1
            return
        
        # Build full question: instruction + passage + question
        full_q_parts = []
        if instruction:
            full_q_parts.append("\n".join(instruction))
        if passage:
            full_q_parts.append("\n".join(passage))
        if q_lines:
            full_q_parts.append("\n".join(q_lines))
        
        q_text = "\n".join(full_q_parts).strip()
        q_text = q_text.replace('\t', ' _____ ').replace('\xa0', ' ')
        
        cleaned = [c.replace('\xa0', ' ').replace('\t', ' ').strip() for c in current_choices]
        if cleaned or q_text:
            problems.append({
                "id": f"{topicId}-{counter[0]+1}",
                "topicId": topicId,
                "question": q_text,
                "choices": cleaned,
                "answer": current_answer,
                "type": "multiple-choice" if cleaned else "essay",
                "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
            })
            counter[0] += 1
        current_q.clear()
        current_choices.clear()
        current_answer = -1
    
    i = 0
    while i < len(paras):
        para = paras[i]
        i += 1
        
        if para is None:
            # blank: save if we have choices
            if current_choices:
                save()
            continue
        
        text, bold = para
        
        # Section heading (all caps, short)
        if text.isupper() and len(text) < 100:
            save()
            passage.clear()
            instruction.clear()
            in_reading = False
            instruction.append(text)
            continue
        
        # Instruction line (Choose the / Read the...)
        if re.match(r'^(Choose the|Read the following|Mark the letter)', text, re.I):
            save()
            passage.clear()
            instruction.clear()
            instruction.append(text)
            in_reading = 'Read the following' in text or 'reading' in text.lower()
            continue
        
        # Numbered question: Question X. / Câu X.
        if is_question_start(text):
            # Save previous if it had choices
            if current_choices:
                save()
            elif current_q:
                # A question without choices — might be embedded choices coming
                pass
            # Start new question; keep passage (reading comprehension)
            current_q.clear()
            current_choices.clear()
            current_answer = -1
            current_q.append(text)
            continue
        
        # Choice line: tab-separated A. B. C. D. (all on one line)
        if is_all_choices_line(text):
            if not current_q and not passage:
                # Phonetics/stress: instruction is set, no question number
                # Each choice line = one independent question
                choices, answer = split_choices_line(text, bold)
                problems.append({
                    "id": f"{topicId}-{counter[0]+1}",
                    "topicId": topicId,
                    "question": "\n".join(instruction),
                    "choices": choices,
                    "answer": answer,
                    "type": "multiple-choice",
                    "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
                })
                counter[0] += 1
            elif current_q:
                # Grammar question: choices follow question text
                choices, answer = split_choices_line(text, bold)
                current_choices = choices
                current_answer = answer
                save()
            elif passage and not current_q:
                # Reading: choices for sub-question without explicit Q label
                choices, answer = split_choices_line(text, bold)
                current_choices = choices
                current_answer = answer
                save()
            continue
        
        # Single choice line starting with A. / B. / C. / D.
        if starts_with_choice(text):
            choices, answer = split_choices_line(text, bold)
            current_choices.extend(choices)
            if answer != -1:
                current_answer = len(current_choices) - len(choices) + answer
            # If this starts with A. it's a new question's choices
            if text.strip().startswith('A.') and len(current_choices) > 4:
                # Shouldn't happen in well-formed data, but safeguard
                pass
            if len(current_choices) >= 4:
                save()
            continue
        
        # Otherwise: passage/context text or continuation of question
        if in_reading or (instruction and not is_question_start(text)):
            # Is it passage text or answer text for reading questions?
            # If we have a current question, it might be answer options without A. prefix
            if current_q and not current_choices:
                # Could be non-labeled choice (happens in some reading Qs)
                current_q.append(text)
            else:
                # Passage accumulation
                passage.append(text)
        else:
            # Grammar question text (no question number, just fill-in-blank)
            if current_choices:
                save()
            current_q.append(text)
    
    save()
    return problems


# ─── Main ─────────────────────────────────────────────────────────────────────

SUBJECTS = [
    {
        "file": "E:\\toanvui-main\\Đề cương ôn thi lớp 7\\Tin học.docx",
        "topicId": "g7-tin",
        "parser": "tin",
    },
    {
        "file": "E:\\toanvui-main\\Đề cương ôn thi lớp 7\\Tiếng Anh.docx",
        "topicId": "g7-english",
        "parser": "english",
    },
]


def run():
    problems_path = "E:\\toanvui-main\\src\\data\\problems.js"
    topics_path   = "E:\\toanvui-main\\src\\data\\topics.js"

    with open(problems_path, encoding="utf-8") as f:
        prob_dict = json.loads(f.read().replace("export const problems = ", "").rstrip(";\n "))

    with open(topics_path, encoding="utf-8") as f:
        top_dict = json.loads(f.read().replace("export const topics = ", "").rstrip(";\n "))

    for subj in SUBJECTS:
        tid = subj["topicId"]
        print(f"\n--- {tid} ---")
        paras = get_paras(subj["file"])
        
        if subj["parser"] == "tin":
            new_probs = parse_tin(paras, tid)
        else:
            new_probs = parse_english(paras, tid)
        
        mc  = sum(1 for p in new_probs if p["type"] == "multiple-choice")
        ans = sum(1 for p in new_probs if p["answer"] != -1)
        print(f"  Parsed {len(new_probs)} problems ({mc} MC, {ans} with answer)")

        debug_path = f"E:\\toanvui-main\\scratch\\{tid}_parsed_v3.json"
        with open(debug_path, "w", encoding="utf-8") as f:
            json.dump(new_probs, f, ensure_ascii=False, indent=2)

        # Remove old
        old = [k for k in prob_dict if k.startswith(tid + "-")]
        for k in old: del prob_dict[k]
        print(f"  Removed {len(old)} old problems")

        # Add new
        for p in new_probs:
            prob_dict[p["id"]] = p

        # Update topics
        for topic in top_dict.get("7", []):
            if topic["id"] == tid:
                topic["problemIds"] = [p["id"] for p in new_probs]
                print(f"  Topics updated ({len(new_probs)} IDs)")
                break

    with open(problems_path, "w", encoding="utf-8") as f:
        f.write("export const problems = ")
        json.dump(prob_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("\nproblems.js written.")

    with open(topics_path, "w", encoding="utf-8") as f:
        f.write("export const topics = ")
        json.dump(top_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("topics.js written.")


run()
