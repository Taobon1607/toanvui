import json
import re

def is_choice_line(text):
    # A line is part of choices if it starts with A. or B. or C. or D.
    # Or contains "\tB. " etc.
    return re.search(r'\b[A-D][\.\)]\s+', text)

def process_groups():
    with open(r"E:\toanvui-main\scratch\english_groups.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
        
    problems = []
    
    for group in groups:
        # We need to extract the instruction, question text, and choices
        instruction = []
        
        # We process line by line
        current_q_text = []
        current_choices = []
        current_answer = -1
        
        def save_problem():
            nonlocal current_q_text, current_choices, current_answer
            if current_choices:
                # build the question text
                q = "\n".join(instruction + current_q_text).strip()
                if not q:
                    q = "Chọn đáp án đúng nhất."
                problems.append({
                    "id": f"g7-english-{len(problems)+1}",
                    "topicId": "g7-english",
                    "question": q,
                    "choices": current_choices,
                    "answer": current_answer,
                    "type": "multiple-choice"
                })
            current_q_text = []
            current_choices = []
            current_answer = -1

        i = 0
        while i < len(group):
            line = group[i]
            text = line["text"]
            
            if is_choice_line(text) or (current_choices and not current_q_text and text.startswith("C.")):
                # This line contains choices!
                # If we don't have A., but it's part of choices
                
                # Split choices
                parts = re.split(r'\b([A-D][\.\)])\s+', text)
                if len(parts) > 1:
                    first_part = parts[0].strip()
                    if first_part and not current_choices:
                        current_q_text.append(first_part)
                    
                    for j in range(1, len(parts), 2):
                        choice_letter = parts[j]
                        choice_content = parts[j+1].strip()
                        full_choice = f"{choice_letter} {choice_content}"
                        current_choices.append(full_choice)
                        
                        # Check bold
                        if line["bold_text"] and line["bold_text"] in full_choice:
                            current_answer = len(current_choices) - 1
                            
                    # Some choices might be split across two lines, like:
                    # Line 1: A. xxx B. yyy
                    # Line 2: C. zzz D. www
                    # If the next line is also a choice line AND we haven't reached 4 choices, we can continue without saving.
                    # BUT what if it's the Phonetics section? 
                    # Phonetics:
                    # Line 1: A. year B. wear C. appear D. hear
                    # Line 2: A. natural B. poverty C. question D. future
                    # In this case, Line 1 has 4 choices. If current_choices has >= 4, it's a complete question!
                    if len(current_choices) >= 4:
                        save_problem()
                else:
                    # Wait, if it didn't split, it might be a weird case
                    if current_choices:
                        current_choices[-1] += " " + text
            else:
                # Not a choice line
                # If we already have choices, maybe it's a new question starting without A. B.? No.
                # It's probably question text.
                if current_choices:
                    # If we had choices, and now see text, we should save the previous problem
                    save_problem()
                    instruction = [] # reset instruction for the next block
                    current_q_text.append(text)
                else:
                    if text.isupper() or "Choose the" in text or "Read the following" in text:
                        instruction.append(text)
                    else:
                        current_q_text.append(text)
            
            i += 1
            
        save_problem()
        
    out_path = r"E:\toanvui-main\scratch\english_problems.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"Generated {len(problems)} problems")

process_groups()
