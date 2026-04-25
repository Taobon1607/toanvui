"""
Universal DOCX parser for Grade 7 review subjects.
Handles: Tin học, Lịch Sử & Địa Lý
Same logic as better_parser.py for Tiếng Anh.
"""
import json
import re
from docx import Document

SUBJECTS = [
    {
        "file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx",
        "topicId": "g7-tin",
        "prefix": "g7-tin",
    },
    {
        "file": r"E:\toanvui-main\Đề cương ôn thi lớp 7\Lịch Sử Địa Lý.docx",
        "topicId": "g7-lichsu",
        "prefix": "g7-lichsu",
    },
]

def get_groups(filepath):
    """Split document paragraphs into groups separated by blank lines."""
    doc = Document(filepath)
    groups = []
    current_group = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            if current_group:
                groups.append(current_group)
                current_group = []
        else:
            is_bold = any(run.bold and run.text.strip() for run in para.runs)
            bold_text = "".join(run.text for run in para.runs if run.bold).strip()
            current_group.append({
                "text": text,
                "is_bold": is_bold,
                "bold_text": bold_text,
            })
    if current_group:
        groups.append(current_group)
    return groups


def is_choice_indicator(text):
    """True if line contains A. B. C. D. pattern."""
    return bool(re.search(r'\b[A-D][\.\)]\s+', text))


def parse_groups(groups, topicId, prefix):
    problems = []
    counter = [0]

    def make_id():
        counter[0] += 1
        return f"{prefix}-{counter[0]}"

    for group in groups:
        instruction = []
        current_q = []
        current_choices = []
        current_answer = -1

        def save():
            nonlocal current_q, current_choices, current_answer
            if not current_q and not current_choices:
                return
            q_text = "\n".join(instruction + current_q).strip()
            # Replace tab characters (blank fill spots) with visible blank marker
            q_text = q_text.replace('\t', ' _____ ')
            if not q_text:
                q_text = "Chọn đáp án đúng nhất."
            cleaned_choices = [c.replace('\t', ' ').strip() for c in current_choices]
            problems.append({
                "id": make_id(),
                "topicId": topicId,
                "question": q_text,
                "choices": cleaned_choices,
                "answer": current_answer,
                "type": "multiple-choice" if cleaned_choices else "essay",
                "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
            })
            current_q.clear()
            current_choices.clear()
            current_answer = -1

        for line in group:
            text = line["text"]
            bold = line["bold_text"]

            # Instruction line (section header / question type prompt)
            if text.isupper() or re.match(
                r'^(Choose the|Read the|Mark the|Select the|Pick the)', text, re.I
            ):
                save()
                instruction.append(text)
                continue

            # New question: "Question X", "Câu X", or numbered "X."
            if re.match(r'^(Question|Câu|Q\.?)\s*\d+', text, re.I) or \
               re.match(r'^\d+[\.\)]\s+\S', text):
                save()
                current_q.append(text)
                continue

            # Choice line (contains A. B. C. D.)
            if is_choice_indicator(text) or (current_q and '\t' in text):
                # Split on each option letter
                parts = re.split(r'(?=\b[A-D][\.\)]\s+)', text)
                if len(parts) == 1 and '\t' in text:
                    parts = text.split('\t')

                for p in parts:
                    p = p.strip()
                    if not p:
                        continue
                    idx_c = len(current_choices)
                    prefix_letters = ["A. ", "B. ", "C. ", "D. "]
                    if not re.match(r'^[A-D][\.\)]', p) and idx_c < 4:
                        p = prefix_letters[idx_c] + p
                    current_choices.append(p)

                    # Determine if this is the correct answer (bold)
                    if bold:
                        clean_p = re.sub(r'^[A-D][\.\)]\s*', '', p).strip()
                        clean_bold = re.sub(r'^[A-D][\.\)]\s*', '', bold).strip()
                        if clean_bold and (clean_bold in clean_p or clean_p in clean_bold):
                            current_answer = len(current_choices) - 1
                continue

            # Plain text line
            if not current_choices:
                current_q.append(text)
            else:
                # Extra text after choices started = part of next question
                save()
                current_q.append(text)

        save()

    return problems


def run():
    # Load current problems.js
    problems_path = r"E:\toanvui-main\src\data\problems.js"
    topics_path = r"E:\toanvui-main\src\data\topics.js"

    with open(problems_path, encoding="utf-8") as f:
        prob_js = f.read()
    prob_dict = json.loads(prob_js.replace("export const problems = ", "").rstrip(";\n "))

    with open(topics_path, encoding="utf-8") as f:
        top_js = f.read()
    top_dict = json.loads(top_js.replace("export const topics = ", "").rstrip(";\n "))

    for subj in SUBJECTS:
        print(f"\n--- Processing {subj['topicId']} ---")
        try:
            groups = get_groups(subj["file"])
        except Exception as e:
            print(f"  ERROR reading file: {e}")
            continue

        new_problems = parse_groups(groups, subj["topicId"], subj["prefix"])
        print(f"  Parsed {len(new_problems)} problems")

        # Save debug json
        debug_path = rf"E:\toanvui-main\scratch\{subj['prefix']}_parsed.json"
        with open(debug_path, "w", encoding="utf-8") as f:
            json.dump(new_problems, f, ensure_ascii=False, indent=2)

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
    print("\nproblems.js written.")

    with open(topics_path, "w", encoding="utf-8") as f:
        f.write("export const topics = ")
        json.dump(top_dict, f, ensure_ascii=False, indent=2)
        f.write(";\n")
    print("topics.js written.")


run()
