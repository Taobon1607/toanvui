import json
import re
import docx2txt
import os

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

# Extract English real questions
english_problems = [v for k, v in problems.items() if k.startswith("g7-english")]
math_problems = [v for k, v in problems.items() if k.startswith("g7-math")]

print(f"Total English problems in DB: {len(english_problems)}")
print(f"Total Math problems in DB: {len(math_problems)}")

# Parse Answer Keys
ans_dir = r"d:\toanvui-main\toanvui-main\Đáp án đề cương"
en_ans_text = docx2txt.process(os.path.join(ans_dir, "TiengAnh7_DapAn.docx"))
math_ans_text = docx2txt.process(os.path.join(ans_dir, "Toan7_DapAn.docx"))

# Find pattern for English answers: "1. B", "2. A"
en_answers = {}
for line in en_ans_text.split('\n'):
    line = line.strip()
    match = re.match(r'^(\d+)\.\s*([A-D])\s*(.*)', line)
    if match:
        en_answers[int(match.group(1))] = {
            "answer": match.group(2),
            "step": match.group(3).strip()
        }
print(f"Found {len(en_answers)} English MCQ answers.")

math_answers = {}
for line in math_ans_text.split('\n'):
    line = line.strip()
    match = re.match(r'^(\d+)\.\s*([A-D])\s*(.*)', line)
    if match:
        math_answers[int(match.group(1))] = {
            "answer": match.group(2),
            "step": match.group(3).strip()
        }
print(f"Found {len(math_answers)} Math MCQ answers.")

