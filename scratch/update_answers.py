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
            # sometimes the step explanation is on the next line
            if not step_text and i + 1 < len(lines):
                next_line = lines[i+1].strip()
                if not re.match(r'^\d+\.', next_line):
                    step_text = next_line
            answers[q_num] = {
                "answer": ord(ans_char) - ord('A'),
                "step": f"Đáp án: {ans_char}. {step_text}".strip()
            }
    return answers

en_answers = parse_mcq_answers(en_ans_text)
math_answers = parse_mcq_answers(math_ans_text)

# Heuristic mapping
def update_problems(subject_prefix, answers, problems):
    updated = 0
    # Collect all problems for this subject
    subj_problems = [v for k, v in problems.items() if k.startswith(subject_prefix)]
    
    # Many parsed problems have "question" text starting with "Question X", "Câu X", or "X."
    for p in subj_problems:
        q_text = p["question"]
        match = re.search(r'^(?:Câu|Question|Bài)?\s*(\d+)[:.]?\s+', q_text, re.IGNORECASE)
        # If it doesn't start with it, maybe it's just the number
        if not match:
             match = re.match(r'^(\d+)\s', q_text)
             
        if match:
            q_num = match.group(1)
            if q_num in answers and len(p.get("choices", [])) > 0:
                p["answer"] = answers[q_num]["answer"]
                p["steps"] = [{"text": answers[q_num]["step"], "highlight": None}]
                updated += 1
    return updated

upd_en = update_problems("g7-english", en_answers, problems)
upd_math = update_problems("g7-math", math_answers, problems)

print(f"Updated {upd_en} English questions and {upd_math} Math questions.")

# Reconstruct the JS file
new_problems_js = ""
for key, value in problems.items():
    new_problems_js += f'  "{key}": {json.dumps(value, ensure_ascii=False, indent=2)},\n'

final_content = "export const problems = {\n" + new_problems_js.rstrip(",\n") + "\n};\n"
with open(problems_file, "w", encoding="utf-8") as f:
    f.write(final_content)
    
print("Successfully written back to problems.js.")
