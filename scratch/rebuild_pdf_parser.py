import fitz
import re
import json
import os
import docx2txt
import uuid

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"
ans_dir = r"d:\toanvui-main\toanvui-main\Đáp án đề cương"

# 1. Parse Answer Keys (reuse the previous logic)
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

# 2. Context-Aware PDF Parsing
def advanced_pdf_parser(filepath, topic_id, mcq_keys, essay_keys):
    doc = fitz.open(filepath)
    problems = []
    
    current_section = ""
    current_q = None
    
    images_info = []
    # Collect all images
    for page_num in range(len(doc)):
        page = doc[page_num]
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            rects = page.get_image_rects(xref)
            if rects:
                rect = rects[0]
                filename = f"img_{uuid.uuid4().hex[:8]}.{ext}"
                out_path = os.path.join(r"d:\toanvui-main\toanvui-main\public\images\g7_exams", filename)
                with open(out_path, "wb") as f:
                    f.write(image_bytes)
                images_info.append({
                    "src": f"/images/g7_exams/{filename}",
                    "y0": rect.y0,
                    "y1": rect.y1,
                    "page": page_num
                })

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if b["type"] == 0:
                for line_obj in b["lines"]:
                    text = "".join([span["text"] for span in line_obj["spans"]]).strip()
                    if not text: continue
                    
                    bbox = line_obj["bbox"]
                    line_y0, line_y1 = bbox[1], bbox[3]
                    
                    matched_images = []
                    for img_info in images_info[:]:
                        if img_info["page"] == page_num and img_info["y0"] >= line_y0 - 20 and img_info["y0"] <= line_y1 + 150:
                            matched_images.append(img_info["src"])
                            images_info.remove(img_info)
                    
                    # Detect Section Headers (e.g. "I. Choose the word...", "II. Mark the letter...")
                    # Or "PRACTICE", "PHONETICS"
                    if re.match(r'^(I|II|III|IV|V|VI)\.\s+[A-Z]', text) or re.match(r'^([A-Z\s]+)$', text):
                        # It's a section header. Only keep if it's long enough or looks like an instruction
                        if len(text) > 10 and not re.match(r'^[A-D]\.\s+', text):
                            current_section = text
                            continue

                    # Detect Question: "1.", "Câu 1:", "Question 1:", "Bài 1:"
                    # BUT NOT if it starts with A. B. C. D.
                    match_q = re.match(r'^(?:Câu|Question|Bài)?\s*(\d+)[:.]?\s+(.*)', text, re.IGNORECASE)
                    
                    if match_q:
                        if current_q:
                            problems.append(current_q)
                        
                        q_num = match_q.group(1)
                        q_rest = match_q.group(2).strip()
                        
                        # Check if q_rest contains A. B. C. D. inline (like "A. year B. wear...")
                        choices = []
                        if re.search(r'\b[A-D][\.\)]\s+', q_rest):
                            question_text = f"{current_section}\n{q_num}." if current_section else f"{q_num}."
                            
                            parts = re.split(r'\b([A-D][\.\)]\s+)', q_rest)
                            choice_text = ""
                            for part in parts:
                                if re.match(r'^[A-D][\.\)]\s+', part):
                                    choice_text = part
                                elif choice_text:
                                    choices.append(part.strip())
                                    choice_text = ""
                        else:
                            question_text = f"{current_section}\n{q_num}. {q_rest}" if current_section else f"{q_num}. {q_rest}"
                        
                        current_q = {
                            "id": f"{topic_id}-{q_num}",
                            "topicId": topic_id,
                            "q_num": q_num, # temp to map answers
                            "question": question_text.strip(),
                            "choices": choices,
                            "answer": 0,
                            "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}],
                            "images": matched_images
                        }
                        continue
                    
                    if current_q:
                        # Detect Choices on new lines
                        if re.search(r'\b[A-D][\.\)]\s+', text):
                            parts = re.split(r'\b([A-D][\.\)]\s+)', text)
                            choice_text = ""
                            for part in parts:
                                if re.match(r'^[A-D][\.\)]\s+', part):
                                    choice_text = part
                                elif choice_text:
                                    current_q["choices"].append(part.strip())
                                    choice_text = ""
                            current_q["images"].extend(matched_images)
                        else:
                            # Append to question text
                            current_q["question"] += "\n" + text
                            current_q["images"].extend(matched_images)
                            
    if current_q:
        problems.append(current_q)

    # Clean up choices and apply answers
    final_problems = []
    for p in problems:
        q_num = p["q_num"]
        del p["q_num"]
        
        if p["choices"]:
            p["type"] = "mcq"
        else:
            p["type"] = "essay"
            
        if p["type"] == "mcq" and q_num in mcq_keys:
            p["answer"] = mcq_keys[q_num]["answer"]
            p["steps"] = [{"text": mcq_keys[q_num]["step"], "highlight": None}]
        elif p["type"] == "essay" and q_num in essay_keys:
            p["steps"] = [{"text": essay_keys[q_num], "highlight": None}]
            
        # Add all problems that look like actual exam questions
        if p["choices"] or len(p["question"]) > 20:
            final_problems.append(p)
            
    return final_problems

# 3. Process
print("Parsing English...")
en_problems = advanced_pdf_parser(os.path.join(files_dir, "Tiếng Anh.pdf"), "g7-english", en_mcq_answers, en_essay_answers)
print("Parsing Math...")
math_problems = advanced_pdf_parser(os.path.join(files_dir, "Toán.pdf"), "g7-math", math_mcq_answers, math_essay_answers)

# Filter duplicates just in case (sometimes same question number appears twice due to review sections vs actual test)
# Since the actual test usually is at the end, we can keep the last occurrence or just keep all.
# The user wants "đảm bảo đủ", so we keep all, but give them unique IDs.
def unique_ids(problems):
    seen = {}
    for p in problems:
        base_id = p["id"]
        if base_id in seen:
            seen[base_id] += 1
            p["id"] = f"{base_id}-{seen[base_id]}"
        else:
            seen[base_id] = 1
    return problems

en_problems = unique_ids(en_problems)
math_problems = unique_ids(math_problems)

# 4. Update problems.js
problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
db_problems = json.loads(json_str)

keys_to_delete = [k for k in db_problems.keys() if k.startswith("g7-english") or k.startswith("g7-math")]
for k in keys_to_delete:
    del db_problems[k]

for p in en_problems:
    db_problems[p["id"]] = p
for p in math_problems:
    db_problems[p["id"]] = p

new_problems_js = ""
for key, value in db_problems.items():
    new_problems_js += f'  "{key}": {json.dumps(value, ensure_ascii=False, indent=2)},\n'

final_content = "export const problems = {\n" + new_problems_js.rstrip(",\n") + "\n};\n"
with open(problems_file, "w", encoding="utf-8") as f:
    f.write(final_content)
    
# 5. Update topics.js to reflect the actual IDs
topics_file = r"d:\toanvui-main\toanvui-main\src\data\topics.js"
with open(topics_file, "r", encoding="utf-8") as f:
    topics_content = f.read()
topics_json_str = topics_content[topics_content.find("["):topics_content.rfind("]")+1]
topics = json.loads(topics_json_str)

for t in topics:
    if t["id"] == "g7-english":
        t["problemIds"] = [p["id"] for p in en_problems]
    elif t["id"] == "g7-math-new":
        t["problemIds"] = [p["id"] for p in math_problems]

topics_js = "export const topics = " + json.dumps(topics, ensure_ascii=False, indent=4) + ";\n"
with open(topics_file, "w", encoding="utf-8") as f:
    f.write(topics_js)

print(f"Added {len(en_problems)} English and {len(math_problems)} Math problems.")
print("Successfully written back to problems.js and topics.js.")
