import os
import re
import json
import mammoth
from bs4 import BeautifulSoup
import uuid

def convert_image(image):
    with image.open() as image_bytes:
        image_data = image_bytes.read()
        
        ext = image.content_type.split("/")[-1]
        filename = f"img_{uuid.uuid4().hex[:8]}.{ext}"
        filepath = os.path.join(r"d:\toanvui-main\toanvui-main\public\images\g7_exams", filename)
        
        with open(filepath, "wb") as f:
            f.write(image_data)
            
        return {"src": f"/images/g7_exams/{filename}"}

def parse_docx(filepath, topic_id):
    with open(filepath, "rb") as docx_file:
        result = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.inline(convert_image))
        html = result.value
        
    soup = BeautifulSoup(html, "html.parser")
    
    problems = []
    current_q = None
    
    for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        text = p.get_text(strip=True)
        img_tags = p.find_all('img')
        images = [img['src'] for img in img_tags if img.has_attr('src')]
        
        # Detect Question: "Câu 1:", "Câu 1.", "Bài 1:"
        match_q = re.match(r'^(Câu|Bài)\s*\d+[:.]?\s*(.*)', text, re.IGNORECASE)
        if match_q:
            if current_q:
                # Clean up choices if they are empty
                if not current_q["choices"] and not current_q.get("type") == "essay":
                    current_q["type"] = "essay"
                problems.append(current_q)
                
            current_q = {
                "id": f"{topic_id}-{len(problems)+1}",
                "topicId": topic_id,
                "question": match_q.group(2).strip(),
                "choices": [],
                "answer": 0, # Default to A
                "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}],
                "images": images
            }
            continue
            
        if current_q:
            # Sometime multiple choices are on the same line: "A. xxx B. yyy C. zzz D. www"
            if re.search(r'\b[A-D][\.\)]\s+', text):
                # Split by A., B., C., D.
                parts = re.split(r'\b[A-D][\.\)]\s+', text)
                for part in parts:
                    part = part.strip()
                    if part:
                        current_q["choices"].append(part)
                if images:
                    current_q["images"].extend(images)
            else:
                # Continuation of question or an essay
                if text and not text.lower().startswith('đáp án') and not text.lower().startswith('hướng dẫn'):
                     if current_q["question"]:
                         current_q["question"] += "\n" + text
                     else:
                         current_q["question"] = text
                if images:
                     current_q["images"].extend(images)

    if current_q:
        if not current_q["choices"]:
            current_q["type"] = "essay"
        problems.append(current_q)
        
    return problems

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"
docx_files = [
    ("Công Nghệ.docx", "g7-congnghe"),
    ("GDCD.docx", "g7-gdcd"),
    ("Lịch Sử Địa Lý.docx", "g7-lichsu"),
    ("Tin học.docx", "g7-tin")
]

all_docx_problems = {}

for filename, topic_id in docx_files:
    filepath = os.path.join(files_dir, filename)
    print(f"Processing {filename}...")
    try:
        problems = parse_docx(filepath, topic_id)
        for p in problems:
            all_docx_problems[p["id"]] = p
        print(f"-> Extracted {len(problems)} problems.")
    except Exception as e:
        print(f"-> Error: {e}")

# Save to scratch folder for review
out_path = r"d:\toanvui-main\toanvui-main\scratch\docx_problems.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_docx_problems, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_docx_problems)} DOCX problems to {out_path}")
