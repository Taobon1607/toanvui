import json
import re
import os
from docx import Document

def parse_english_docx(filepath):
    doc = Document(filepath)
    problems = []
    
    current_passage = ""
    collecting_passage = False
    
    instruction_pattern = r"Read the following passage|Mark the letter A, B, C or D|Choose the word"
    question_start_pattern = r"(Question\s*\d+|Câu\s*\d+)[\.:]"
    choice_pattern = r"\b([A-D][\.\)])\s+"

    def create_problem(q_text, choices, answer, type="multiple-choice"):
        if not choices:
            return
        
        full_question = ""
        if current_passage:
            full_question += current_passage + "\n\n"
        full_question += q_text
        
        problems.append({
            "id": f"g7-english-{len(problems)+1}",
            "topicId": "g7-english",
            "question": full_question.strip(),
            "choices": choices,
            "answer": answer,
            "type": type
        })

    def get_para_data(para):
        # Return list of (text, is_bold) for each run
        data = []
        for run in para.runs:
            data.append((run.text, run.bold))
        return data

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        if re.search(instruction_pattern, text, re.IGNORECASE):
            current_passage = text
            collecting_passage = True
            continue
            
        if collecting_passage:
            if re.search(question_start_pattern, text, re.IGNORECASE) or re.search(choice_pattern, text):
                collecting_passage = False
            else:
                current_passage += "\n" + text
                continue

        # Split by Question marker
        q_chunks = re.split(r'\b(Question\s*\d+|Câu\s*\d+)[\.:]', text, flags=re.IGNORECASE)
        
        if len(q_chunks) > 1:
            # Multi-question paragraph
            # We need to find which choices are bold. 
            # Since we split the text, we'll use a more robust way to match bold runs to choices.
            para_runs = get_para_data(para)
            
            for i in range(1, len(q_chunks), 2):
                q_num_text = q_chunks[i]
                q_body = q_chunks[i+1].strip()
                
                parts = re.split(choice_pattern, q_body)
                choices = []
                answer = 0
                
                q_question_text = q_num_text + ". " + parts[0].strip()
                
                for j in range(1, len(parts), 2):
                    c_letter = parts[j]
                    c_text = parts[j+1].strip()
                    full_c = f"{c_letter} {c_text}"
                    choices.append(full_c)
                    
                    # Check if this choice text was bolded in the original runs
                    # We look for c_text in the runs
                    choice_is_bold = False
                    for run_text, is_bold in para_runs:
                        if is_bold and c_text in run_text and len(run_text.strip()) > 1:
                            # Avoid matching "Question X" bolding
                            if "Question" not in run_text:
                                choice_is_bold = True
                                break
                    if choice_is_bold:
                        answer = len(choices) - 1
                
                create_problem(q_question_text, choices, answer)
        else:
            parts = re.split(choice_pattern, text)
            if len(parts) > 1:
                para_runs = get_para_data(para)
                choices = []
                answer = 0
                q_text = parts[0].strip()
                
                for j in range(1, len(parts), 2):
                    c_letter = parts[j]
                    c_text = parts[j+1].strip()
                    full_c = f"{c_letter} {c_text}"
                    choices.append(full_c)
                    
                    choice_is_bold = False
                    for run_text, is_bold in para_runs:
                        if is_bold and c_text in run_text and len(run_text.strip()) > 1:
                            if "Question" not in run_text:
                                choice_is_bold = True
                                break
                    if choice_is_bold:
                        answer = len(choices) - 1
                
                create_problem(q_text or "Câu hỏi:", choices, answer)
            else:
                if not collecting_passage:
                    current_passage = text 
    
    out_path = r"E:\toanvui-main\scratch\english_parsed_v3.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(problems)} problems")

if __name__ == "__main__":
    parse_english_docx(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx")
