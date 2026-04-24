import json
import re
import docx2txt
import os
import fitz

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"
ans_dir = r"d:\toanvui-main\toanvui-main\Đáp án đề cương"

# 1. Parse Answer Keys
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

en_ans_text = docx2txt.process(os.path.join(ans_dir, "TiengAnh7_DapAn.docx"))
math_ans_text = docx2txt.process(os.path.join(ans_dir, "Toan7_DapAn.docx"))

en_mcq_answers = parse_mcq_answers(en_ans_text)
math_mcq_answers = parse_mcq_answers(math_ans_text)
en_essay_answers = parse_essay_answers(en_ans_text, r'^Question\s+(\d+)\.\s*(.*)')
math_essay_answers = parse_essay_answers(math_ans_text, r'^Bài\s+(\d+)\.\s*(.*)')

# 2. Extract texts and Question Numbers from PDFs
def extract_q_numbers_from_pdf(pdf_file):
    doc = fitz.open(os.path.join(files_dir, pdf_file))
    q_map = {} # text -> q_num
    
    current_q_num = None
    current_text = ""
    for page in doc:
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            if b["type"] == 0:
                for line_obj in b["lines"]:
                    text = "".join([span["text"] for span in line_obj["spans"]]).strip()
                    if not text: continue
                    
                    match_q = re.match(r'^(Câu|Question|Bài)?\s*(\d+)[:.]?\s+(.*)', text, re.IGNORECASE)
                    if match_q:
                        if current_q_num and current_text:
                            q_map[current_text] = current_q_num
                        current_q_num = match_q.group(2)
                        current_text = match_q.group(3).strip()
                    elif current_q_num:
                        current_text += "\n" + text
    if current_q_num and current_text:
        q_map[current_text] = current_q_num
    return q_map

en_pdf_map = extract_q_numbers_from_pdf("Tiếng Anh.pdf")
math_pdf_map = extract_q_numbers_from_pdf("Toán.pdf")

# 3. Update problems.js
problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

def clean_text(t):
    return re.sub(r'\s+', '', t).lower()

en_pdf_clean = {clean_text(k): v for k, v in en_pdf_map.items()}
math_pdf_clean = {clean_text(k): v for k, v in math_pdf_map.items()}

updated_en = 0
updated_math = 0

for pid, p in problems.items():
    if pid.startswith("g7-english"):
        q_clean = clean_text(p["question"])
        # Find matching question in PDF map
        q_num = None
        for k_clean, v_num in en_pdf_clean.items():
            if q_clean.startswith(k_clean[:50]) or k_clean.startswith(q_clean[:50]): # fuzzy match prefix
                q_num = v_num
                break
        if q_num:
            is_mcq = len(p.get("choices", [])) > 0
            if is_mcq and q_num in en_mcq_answers:
                p["answer"] = en_mcq_answers[q_num]["answer"]
                p["steps"] = [{"text": en_mcq_answers[q_num]["step"], "highlight": None}]
                updated_en += 1
            elif not is_mcq and q_num in en_essay_answers:
                p["steps"] = [{"text": en_essay_answers[q_num], "highlight": None}]
                updated_en += 1

    elif pid.startswith("g7-math"):
        q_clean = clean_text(p["question"])
        q_num = None
        for k_clean, v_num in math_pdf_clean.items():
            if q_clean.startswith(k_clean[:50]) or k_clean.startswith(q_clean[:50]):
                q_num = v_num
                break
        if q_num:
            is_mcq = len(p.get("choices", [])) > 0
            if is_mcq and q_num in math_mcq_answers:
                p["answer"] = math_mcq_answers[q_num]["answer"]
                p["steps"] = [{"text": math_mcq_answers[q_num]["step"], "highlight": None}]
                updated_math += 1
            elif not is_mcq and q_num in math_essay_answers:
                p["steps"] = [{"text": math_essay_answers[q_num], "highlight": None}]
                updated_math += 1

print(f"Updated English: {updated_en}")
print(f"Updated Math: {updated_math}")

new_problems_js = ""
for key, value in problems.items():
    new_problems_js += f'  "{key}": {json.dumps(value, ensure_ascii=False, indent=2)},\n'

final_content = "export const problems = {\n" + new_problems_js.rstrip(",\n") + "\n};\n"
with open(problems_file, "w", encoding="utf-8") as f:
    f.write(final_content)
    
print("Successfully written back to problems.js.")
