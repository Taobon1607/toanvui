import json
import re
from docx import Document

def parse_docx_to_problems(filepath):
    doc = Document(filepath)
    problems = []
    
    current_text = []
    current_choices = []
    current_answer = 0
    
    def save_problem():
        nonlocal current_text, current_choices, current_answer
        # Clean up text
        q_text = "\n".join(current_text).strip()
        # If there's no question text but there are choices (like phonetics), we just use the choices.
        if not q_text and not current_choices:
            return
            
        if not current_choices:
            # It's an essay or reading passage. But user said correct answer is bolded, so it must be multiple choice.
            # We skip empty ones
            pass
        else:
            problems.append({
                "id": f"g7-english-{len(problems)+1}",
                "topicId": "g7-english",
                "question": q_text,
                "choices": current_choices,
                "answer": current_answer,
                "type": "multiple-choice"
            })
            
        current_text = []
        current_choices = []
        current_answer = 0

    instruction_text = ""

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            # User said "phân tách các câu hỏi bằng xuống dòng" -> newline separates questions
            if current_text or current_choices:
                save_problem()
            continue
            
        # Is this an instruction?
        if text.isupper() or text.startswith("Choose the word"):
            # If we already have something, save it
            if current_text or current_choices:
                save_problem()
            instruction_text = text
            continue

        # Extract choices from this paragraph
        # A paragraph might contain one or more choices: "A. xxx B. yyy"
        # We need to detect if it has A., B., C., D.
        # Also, check for bold text to find the answer.
        
        # Let's see if the paragraph starts with A., B., C., D. or Question X.
        if re.match(r'^(Question\s*\d+|Câu\s*\d+)[\.:]', text, re.IGNORECASE):
            if current_text or current_choices:
                save_problem()
            # It's a new question
            # Sometimes the question and choices are in the same line?
        
        # Collect bold text to identify answer
        bold_texts = []
        for run in para.runs:
            if run.bold and run.text.strip():
                bold_texts.append(run.text.strip())
                
        # Does this line contain choices?
        # A choice is typically A. or B. or C. or D.
        # We can split by A., B., C., D.
        # However, to be safe, if we see A. and it's after the question, we parse it.
        # Let's simplify: if the line has A. or B. or C. or D., it might be choices.
        parts = re.split(r'\b([A-D][\.\)])\s+', text)
        if len(parts) > 1:
            # It has choices!
            # If we haven't seen choices yet for this question, but we see A., B., C., D.
            # wait, if the paragraph starts with something else, the first part is question text.
            first_part = parts[0].strip()
            if first_part:
                current_text.append(first_part)
            
            for i in range(1, len(parts), 2):
                choice_letter = parts[i]
                choice_content = parts[i+1].strip()
                full_choice = f"{choice_letter} {choice_content}"
                current_choices.append(full_choice)
                
                # Check if this choice contains the bold text
                is_bold = False
                for b in bold_texts:
                    if b in full_choice and len(b) > 1:
                        is_bold = True
                        break
                # If the run itself was bold, we can also check
                # But matching text is usually enough. Wait, what if bold_texts is just "A."?
                if is_bold:
                    current_answer = len(current_choices) - 1
        else:
            # No A. B. C. D. found in this line.
            # If we already have choices, maybe this is a continuation? Or a new question?
            # User said "phân tách bằng xuống dòng", so it's part of the same question if no empty line!
            if current_choices:
                # continuation of the last choice? or a new paragraph for question?
                # Actually, if we already have choices, it might be a new question that doesn't have choices yet (error in doc)
                # But let's just append to question text if no choices, else append to last choice
                current_choices[-1] += " " + text
            else:
                current_text.append(text)

    if current_text or current_choices:
        save_problem()

    # Post process to prepend instructions if question text is empty
    for p in problems:
        if not p["question"]:
            p["question"] = instruction_text

    out_path = r"E:\toanvui-main\scratch\english_parsed.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(problems)} problems")

parse_docx_to_problems(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx")
