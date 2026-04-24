import fitz  # PyMuPDF
import os
import re
import json
import uuid

def parse_pdf(filepath, topic_id):
    doc = fitz.open(filepath)
    problems = []
    current_q = None
    
    # We will process page by page
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Extract Images
        # We get a list of images on the page
        images_info = []
        for img in page.get_images(full=True):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            
            # Find coordinates of the image on the page
            # PyMuPDF get_image_rects returns a list of Rects where this image is displayed
            rects = page.get_image_rects(xref)
            if rects:
                rect = rects[0]
                
                # Save the image
                filename = f"img_{uuid.uuid4().hex[:8]}.{ext}"
                out_path = os.path.join(r"d:\toanvui-main\toanvui-main\public\images\g7_exams", filename)
                with open(out_path, "wb") as f:
                    f.write(image_bytes)
                
                images_info.append({
                    "src": f"/images/g7_exams/{filename}",
                    "y0": rect.y0,
                    "y1": rect.y1
                })

        # 2. Extract Text Blocks
        blocks = page.get_text("blocks")
        # Sort blocks vertically, then horizontally
        blocks.sort(key=lambda b: (b[1], b[0]))
        
        for b in blocks:
            # block format: (x0, y0, x1, y1, "text", block_no, block_type)
            # block_type 0 means text
            if b[6] == 0:
                text = b[4].strip()
                if not text: continue
                
                # Find images that overlap vertically with this text block
                # Or are just below it. A simple heuristic: if image's y0 is within 50px of text's y1
                block_y0, block_y1 = b[1], b[3]
                matched_images = []
                for img_info in images_info[:]:
                    if img_info["y0"] >= block_y0 - 20 and img_info["y0"] <= block_y1 + 100:
                        matched_images.append(img_info["src"])
                        images_info.remove(img_info) # don't match again
                
                # Detect Question: "Câu 1", "Question 1", "1."
                # Be careful not to match random numbers. Usually "Câu \d" or "\d\." at start of line
                match_q = re.match(r'^(Câu|Question)?\s*(\d+)[:.]?\s*(.*)', text, re.IGNORECASE | re.DOTALL)
                if match_q:
                    if current_q:
                        if not current_q["choices"] and not current_q.get("type") == "essay":
                            current_q["type"] = "essay"
                        problems.append(current_q)
                        
                    current_q = {
                        "id": f"{topic_id}-{match_q.group(2)}",
                        "topicId": topic_id,
                        "question": match_q.group(3).strip(),
                        "choices": [],
                        "answer": 0,
                        "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}],
                        "images": matched_images
                    }
                    continue
                
                if current_q:
                    # Detect Choices A., B., C., D.
                    # Text might have multiple choices: "A. xxx B. yyy"
                    if re.search(r'\b[A-D][\.\)]\s+', text):
                        parts = re.split(r'\b[A-D][\.\)]\s+', text)
                        for part in parts:
                            part = part.strip()
                            if part:
                                current_q["choices"].append(part)
                        current_q["images"].extend(matched_images)
                    else:
                        # Append to question
                        if text and not text.lower().startswith('đáp án'):
                            current_q["question"] += "\n" + text
                        current_q["images"].extend(matched_images)

    if current_q:
        if not current_q["choices"]:
            current_q["type"] = "essay"
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
        problems = parse_pdf(filepath, topic_id)
        # Deduplicate IDs (sometimes same question number appears in different parts)
        unique_problems = {}
        idx = 1
        for p in problems:
            pid = f"{topic_id}-{idx}"
            p["id"] = pid
            all_pdf_problems[pid] = p
            idx += 1
        print(f"-> Extracted {len(problems)} problems.")
    except Exception as e:
        print(f"-> Error: {e}")

out_path = r"d:\toanvui-main\toanvui-main\scratch\pdf_problems.json"
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(all_pdf_problems, f, ensure_ascii=False, indent=2)

print(f"Saved {len(all_pdf_problems)} PDF problems to {out_path}")
