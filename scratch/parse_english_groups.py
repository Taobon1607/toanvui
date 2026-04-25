from docx import Document
import json

def parse_english(filepath):
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
            # Check if any run is bold
            is_bold = any(run.bold and run.text.strip() for run in para.runs)
            # Find bold text
            bold_text = "".join(run.text for run in para.runs if run.bold).strip()
            
            current_group.append({
                "text": text,
                "is_bold": is_bold,
                "bold_text": bold_text
            })
            
    if current_group:
        groups.append(current_group)
        
    out_path = r"E:\toanvui-main\scratch\english_groups.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(groups, f, ensure_ascii=False, indent=2)
    print(f"Total groups: {len(groups)}")

parse_english(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx")
