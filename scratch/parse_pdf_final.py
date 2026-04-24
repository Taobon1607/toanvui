import fitz
import os
import re
import json
import uuid

def parse_english_math_pdf_with_images(filepath, topic_id):
    doc = fitz.open(filepath)
    problems = []
    current_q = None
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        
        # 1. Extract Images
        images_info = []
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
                    "y1": rect.y1
                })

        # 2. Extract Text Line by Line using dict to get coordinates
        # page.get_text("dict") returns blocks, lines, spans
        blocks = page.get_text("dict")["blocks"]
        
        for b in blocks:
            if b["type"] == 0:  # text block
                for line_obj in b["lines"]:
                    text = "".join([span["text"] for span in line_obj["spans"]]).strip()
                    if not text: continue
                    
                    bbox = line_obj["bbox"] # [x0, y0, x1, y1]
                    line_y0, line_y1 = bbox[1], bbox[3]
                    
                    matched_images = []
                    for img_info in images_info[:]:
                        # If image is below this line but above next lines...
                        # Heuristic: image is within 150px below the text
                        if img_info["y0"] >= line_y0 - 20 and img_info["y0"] <= line_y1 + 150:
                            matched_images.append(img_info["src"])
                            images_info.remove(img_info)

                    match_q = re.match(r'^(Câu|Question|Bài)?\s*(\d+)[:.]?\s+(.*)', text, re.IGNORECASE)
                    if match_q:
                        if current_q:
                            if not current_q["choices"] and not current_q.get("type") == "essay":
                                current_q["type"] = "essay"
                            if current_q["choices"] or current_q.get("explicit"):
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
                        current_q["explicit"] = bool(match_q.group(1))
                        continue
                    
                    if current_q:
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
                            if text and not text.lower().startswith('đáp án'):
                                current_q["question"] += "\n" + text
                            current_q["images"].extend(matched_images)

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
        problems = parse_english_math_pdf_with_images(filepath, topic_id)
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
