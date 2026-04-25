from docx import Document
import json
import re

def parse_english_docx(filepath):
    doc = Document(filepath)
    
    problems = []
    current_q = {"question": "", "choices": [], "answer": -1}
    
    for para in doc.paragraphs:
        text = para.text.strip()
        
        # Newline separation means a blank paragraph separates questions
        if not text:
            # If we have a question, push it
            if current_q["question"] or current_q["choices"]:
                problems.append(current_q)
                current_q = {"question": "", "choices": [], "answer": -1}
            continue
            
        # If it's a choice line, typically starts with A., B., C., D.
        # It could also be multiple choices on the same line.
        # But wait, the user said they separated by newline and bolded the right answer.
        # Let's extract all text and bold status.
        
        # A paragraph can have multiple runs. A run has .bold property.
        # We can reconstruct the text with bold info.
        
        # To handle choices like "A. ... B. ...", if the line has choices, we might need to split it
        # or we just collect lines for the current question.
        
        # We will just dump the paragraphs with their bold words first to see the exact structure.
        para_data = {
            "text": text,
            "runs": []
        }
        for run in para.runs:
            if run.text.strip():
                para_data["runs"].append({
                    "text": run.text,
                    "bold": run.bold
                })
                
        current_q["choices"].append(para_data)
        
    if current_q["question"] or current_q["choices"]:
        problems.append(current_q)
        
    out_path = r"E:\toanvui-main\scratch\english_debug3.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(problems[:100], f, ensure_ascii=False, indent=2)
    print(f"Dumped {len(problems)} items to {out_path}")

filepath = r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx"
parse_english_docx(filepath)
