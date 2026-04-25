"""
Improved universal DOCX parser for Grade 7 review subjects.
Handles: Tin học, Lịch Sử & Địa Lý
Processes paragraph-by-paragraph (not group-by-blank-line).
"""
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

SUBJECTS = [
    {
        "file": "E:\\toanvui-main\\Đề cương ôn thi lớp 7\\Tin học.docx",
        "topicId": "g7-tin",
        "prefix": "g7-tin",
    },
    {
        "file": "E:\\toanvui-main\\Đề cương ôn thi lớp 7\\Lịch Sử Địa Lý.docx",
        "topicId": "g7-lichsu",
        "prefix": "g7-lichsu",
    },
]


def get_paras(filepath):
    """Return list of (text, bold_text) for non-empty paragraphs."""
    doc = Document(filepath)
    result = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            result.append(None)  # blank line marker
            continue
        bold_text = "".join(r.text for r in para.runs if r.bold).strip()
        result.append((text, bold_text))
    return result


def is_question_start(text):
    return bool(re.match(r'^(Câu\s*\d+|Question\s*\d+|\d+[\.\)]\s+\S)', text, re.I))


def has_choices(text):
    """True if the text contains A. or A) style options."""
    return bool(re.search(r'\b[A-D][.\)]\s*\S', text))


def split_choices_line(text, bold_text):
    """
    Split a single paragraph containing A. B. C. D. into individual choices
    and identify which one is bold.
    Returns list of (choice_text, is_correct).
    """
    # Split on each A. B. C. D. boundary
    parts = re.split(r'(?<!\w)([A-D][\.\)]\s*)', text)
    # parts = ['', 'A. ', 'text A', 'B. ', 'text B', ...]
    choices = []
    i = 1
    while i < len(parts) - 1:
        letter = parts[i].strip()  # e.g. 'A.'
        content = parts[i + 1].strip() if (i + 1) < len(parts) else ''
        # Clean nbsp
        content = content.replace('\xa0', ' ').replace('\t', ' ').strip()
        full = f"{letter} {content}"
        choices.append(full)
        i += 2

    if not choices:
        # Fallback: split by tab
        raw_parts = [p.replace('\xa0', ' ').strip() for p in text.split('\t') if p.strip()]
        prefixes = ["A. ", "B. ", "C. ", "D. "]
        for idx, p in enumerate(raw_parts[:4]):
            if not re.match(r'^[A-D][.\)]', p) and idx < 4:
                p = prefixes[idx] + p
            choices.append(p)

    # Find correct answer
    answer = -1
    if bold_text:
        # Clean bold_text for matching
        clean_bold = re.sub(r'^[A-D][.\)]\s*', '', bold_text).replace('\xa0', ' ').strip()
        for idx, c in enumerate(choices):
            clean_c = re.sub(r'^[A-D][.\)]\s*', '', c).replace('\xa0', ' ').strip()
            # Try substring match: bold must overlap meaningfully
            if clean_bold and len(clean_bold) > 3:
                if clean_bold[:10] in clean_c or clean_c[:10] in clean_bold:
                    answer = idx
                    break

    return choices, answer


def parse_paras(paras, topicId, prefix):
    problems = []
    counter = [0]

    def make_id():
        counter[0] += 1
        return f"{prefix}-{counter[0]}"

    current_q_lines = []
    current_choices = []
    current_answer = -1

    def save():
        nonlocal current_q_lines, current_choices, current_answer
        if not current_q_lines:
            return
        q_text = "\n".join(current_q_lines).strip().replace('\t', ' _____ ').replace('\xa0', ' ')
        cleaned = [c.replace('\xa0', ' ').replace('\t', ' ').strip() for c in current_choices]
        problems.append({
            "id": make_id(),
            "topicId": topicId,
            "question": q_text,
            "choices": cleaned,
            "answer": current_answer,
            "type": "multiple-choice" if cleaned else "essay",
            "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
        })
        current_q_lines.clear()
        current_choices.clear()
        current_answer = -1

    for para in paras:
        if para is None:
            # Blank line: if we're in the middle of a question with choices, save it
            if current_choices:
                save()
            # else keep accumulating question context
            continue

        text, bold_text = para

        # Skip pure section headers (all caps, short)
        if text.isupper() and len(text) < 80 and not re.match(r'^[A-D][.\)]', text):
            continue

        # New question start
        if is_question_start(text):
            if current_choices or (current_q_lines and is_question_start(current_q_lines[0])):
                save()
            # Check if choices are embedded in the same line
            # e.g. "Câu 1: ...? A. x B. y C. z D. w"
            if has_choices(text):
                # Split question from choices
                m = re.search(r'(?<!\w)([A-D][.\)]\s*\S)', text)
                if m:
                    q_part = text[:m.start()].strip()
                    choices_part = text[m.start():]
                    save()  # save any previous
                    current_q_lines.append(q_part)
                    choices, answer = split_choices_line(choices_part, bold_text)
                    current_choices = choices
                    current_answer = answer
                    save()
                    continue
            save()  # save previous if any
            current_q_lines.append(text)
            continue

        # Choice line
        if has_choices(text):
            # Might be continuation of choices (C. D. after A. B.)
            choices, answer = split_choices_line(text, bold_text)
            current_choices.extend(choices)
            if answer != -1:
                current_answer = len(current_choices) - len(choices) + answer
            continue

        # Plain text line
        if current_choices:
            # After choices started: this is context (e.g., image description), append to question
            current_q_lines.append(text)
        else:
            current_q_lines.append(text)

    save()
    return problems


def run():
    problems_path = "E:\\toanvui-main\\src\\data\\problems.js"
    topics_path = "E:\\toanvui-main\\src\\data\\topics.js"

    with open(problems_path, encoding="utf-8") as f:
        prob_js = f.read()
    prob_dict = json.loads(prob_js.replace("export const problems = ", "").rstrip(";\n "))

    with open(topics_path, encoding="utf-8") as f:
        top_js = f.read()
    top_dict = json.loads(top_js.replace("export const topics = ", "").rstrip(";\n "))

    for subj in SUBJECTS:
        print(f"\n--- Processing {subj['topicId']} ---")
        try:
            paras = get_paras(subj["file"])
        except Exception as e:
            print(f"  ERROR reading file: {e}")
            continue

        new_problems = parse_paras(paras, subj["topicId"], subj["prefix"])
        mc = sum(1 for p in new_problems if p['type'] == 'multiple-choice')
        answered = sum(1 for p in new_problems if p['answer'] != -1)
        print(f"  Parsed {len(new_problems)} problems ({mc} MC, {answered} with identified answers)")

        # Save debug json
        debug_path = f"E:\\toanvui-main\\scratch\\{subj['prefix']}_parsed.json"
        with open(debug_path, "w", encoding="utf-8") as f:
            json.dump(new_problems, f, ensure_ascii=False, indent=2)
        print(f"  Debug saved: {debug_path}")

        # Remove old problems for this topic
        old_keys = [k for k in prob_dict if k.startswith(subj["prefix"] + "-")]
        for k in old_keys:
            del prob_dict[k]
        print(f"  Removed {len(old_keys)} old problems")

        # Add new problems
        for p in new_problems:
            prob_dict[p["id"]] = p

        # Update topics.js problemIds
        for topic in top_dict.get("7", []):
            if topic["id"] == subj["topicId"]:
                topic["problemIds"] = [p["id"] for p in new_problems]
                print(f"  Updated topic problemIds ({len(new_problems)} items)")
                break

    # Write back
    with open(problems_path, "w", encoding="utf-8") as f:
        f.write("export const problems = ")
        json.dump(prob_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("\nproblems.js written OK.")

    with open(topics_path, "w", encoding="utf-8") as f:
        f.write("export const topics = ")
        json.dump(top_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("topics.js written OK.")


run()
