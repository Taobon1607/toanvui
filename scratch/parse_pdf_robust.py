import fitz
import os
import re
import json

def parse_english_math_pdf(filepath, topic_id):
    doc = fitz.open(filepath)
    problems = []
    current_q = None
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # Simple text extraction line by line
        text = page.get_text("text")
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        for line in lines:
            # Detect Question
            # Match "Câu 1:", "Question 1:", "1. ", "Bài 1:"
            # We want to be careful with "1." so we check if it looks like a question or if it's in a question section.
            # Actually, "1." followed by some text.
            match_q = re.match(r'^(Câu|Question|Bài)?\s*(\d+)[:.]?\s+(.*)', line, re.IGNORECASE)
            if match_q:
                # If we have a current_q, save it
                if current_q:
                    if not current_q["choices"] and not current_q.get("type") == "essay":
                        current_q["type"] = "essay"
                    # Only append if it seems like a real question (has choices or is explicitly "Câu/Bài")
                    if current_q["choices"] or match_q.group(1):
                         problems.append(current_q)
                    else:
                         # It was just a list item like "1. Traffic", discard
                         pass
                         
                current_q = {
                    "id": f"{topic_id}-{match_q.group(2)}",
                    "topicId": topic_id,
                    "question": match_q.group(3).strip(),
                    "choices": [],
                    "answer": 0,
                    "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
                }
                # Keep track if it explicitly had "Câu" or "Question"
                current_q["explicit"] = bool(match_q.group(1))
                continue
            
            if current_q:
                # Detect Choices A., B., C., D.
                # It can be on one line: "A. xxx B. yyy"
                if re.search(r'\b[A-D][\.\)]\s+', line):
                    parts = re.split(r'\b([A-D][\.\)]\s+)', line)
                    # parts will be ['', 'A. ', 'xxx ', 'B. ', 'yyy']
                    # Reconstruct choices
                    choice_text = ""
                    for part in parts:
                        if re.match(r'^[A-D][\.\)]\s+', part):
                            choice_text = part
                        elif choice_text:
                            current_q["choices"].append(part.strip())
                            choice_text = ""
                else:
                    # Append to question
                    if line and not line.lower().startswith('đáp án'):
                        current_q["question"] += "\n" + line

    if current_q:
        if not current_q["choices"] and not current_q.get("type") == "essay":
            current_q["type"] = "essay"
        if current_q["choices"] or current_q.get("explicit"):
             problems.append(current_q)

    return problems

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"
pdf_files = [
    ("Tiếng Anh.pdf", "g7-english"),
    ("Toán.pdf", "g7-math")
]

all_pdf_problems = {}

for filename, topic_id in pdf_files:
    filepath = os.path.join(files_dir, filename)
    print(f"Processing {filename}...")
    try:
        problems = parse_english_math_pdf(filepath, topic_id)
        # Deduplicate and re-index
        idx = 1
        for p in problems:
            pid = f"{topic_id}-{idx}"
            p["id"] = pid
            if "explicit" in p: del p["explicit"]
            all_pdf_problems[pid] = p
            idx += 1
        print(f"-> Extracted {len(problems)} problems.")
    except Exception as e:
        print(f"-> Error: {e}")

out_path = r"d:\toanvui-main\toanvui-main\scratch\pdf_problems.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_pdf_problems, f, ensure_ascii=False, indent=2)

print(f"Saved PDF problems to {out_path}")
