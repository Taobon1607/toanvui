import json
import re
import docx2txt
import os

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

ans_dir = r"d:\toanvui-main\toanvui-main\Đáp án đề cương"
en_ans_text = docx2txt.process(os.path.join(ans_dir, "TiengAnh7_DapAn.docx"))
math_ans_text = docx2txt.process(os.path.join(ans_dir, "Toan7_DapAn.docx"))

# Extract MCQ answers
def parse_mcq_answers(text):
    answers = {}
    lines = text.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        match = re.match(r'^(\d+)\.\s*([A-D])\s*(.*)', line)
        if match:
            q_num = match.group(1)
            ans_char = match.group(2)
            step_text = match.group(3).strip()
            if not step_text and i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if not re.match(r'^\d+\.', next_line) and not next_line.startswith("Giải thích chi tiết:"):
                    step_text = next_line
            answers[q_num] = {
                "answer": ord(ans_char) - ord('A'),
                "step": f"Đáp án: {ans_char}. {step_text}".strip()
            }
    return answers

en_answers = parse_mcq_answers(en_ans_text)
math_answers = parse_mcq_answers(math_ans_text)

# We also need to extract essay answers for English (Question 36 - 40)
# and Math (Bài 4 - Bài 8)
def parse_essay_answers(text, prefix_pattern):
    answers = {}
    lines = text.split('\n')
    current_q = None
    current_text = ""
    for line in lines:
        match = re.match(prefix_pattern, line, re.IGNORECASE)
        if match:
            if current_q:
                answers[current_q] = current_text.strip()
            current_q = match.group(1)
            current_text = match.group(2).strip()
        elif current_q:
            current_text += "\n" + line.strip()
            
    if current_q:
        answers[current_q] = current_text.strip()
    return answers

en_essays = parse_essay_answers(en_ans_text, r'^Question\s+(\d+)\.\s*(.*)')
math_essays = parse_essay_answers(math_ans_text, r'^Bài\s+(\d+)\.\s*(.*)')

def update_problems(subject_prefix, mcq_answers, essay_answers, problems):
    updated = 0
    subj_problems = [v for k, v in problems.items() if k.startswith(subject_prefix)]
    
    for p in subj_problems:
        match = re.match(r'^g7-[a-z]+-(\d+)$', p["id"])
        if match:
            q_num = match.group(1)
            is_mcq = len(p.get("choices", [])) > 0
            
            if is_mcq and q_num in mcq_answers:
                p["answer"] = mcq_answers[q_num]["answer"]
                p["steps"] = [{"text": mcq_answers[q_num]["step"], "highlight": None}]
                updated += 1
            elif not is_mcq and q_num in essay_answers:
                p["steps"] = [{"text": essay_answers[q_num], "highlight": None}]
                updated += 1
            # If the ID doesn't directly map because of shifted IDs in English,
            # we should look for "Câu X" inside the original text, but we already stripped it.
            # Wait, for English, "g7-english-1" actually corresponds to "1. Traffic", 
            # while the REAL Question 1 corresponds to "g7-english-72".
            # The PDF extracted all numbered lists. Let's look at pdf_problems.json to see what ID corresponds to Question 1 in practice.
    return updated

print(f"Direct ID map update:")
print(f"Updated English: {update_problems('g7-english', en_answers, en_essays, problems)}")
print(f"Updated Math: {update_problems('g7-math', math_answers, math_essays, problems)}")

# The above mapping fails for English because the question numbers in the PDF were reset 
# multiple times (Vocabulary 1..10, Grammar 1..10, Practice 1..40).
# The ID is assigned based on the order it appears in the PDF!
# `parse_pdf_final.py` used an auto-incrementing `idx`:
# pid = f"{topic_id}-{idx}", idx += 1
# So the ID is NOT the question number from the text!
