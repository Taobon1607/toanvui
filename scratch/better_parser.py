import json
import re

def process():
    with open(r"E:\toanvui-main\scratch\english_groups.json", "r", encoding="utf-8") as f:
        groups = json.load(f)
        
    problems = []
    
    for group in groups:
        # Group is a list of lines
        
        # We can split the group into sub-problems by looking for "Question X" or "Câu X"
        # Or by looking for choice lines "A."
        
        # We'll just build problems sequentially
        current_q = []
        current_choices = []
        current_answer = -1
        instruction = []
        
        def save():
            nonlocal current_q, current_choices, current_answer
            if current_q or current_choices:
                q_text = "\n".join(instruction + current_q).strip()
                # Replace \t with blanks in question
                q_text = q_text.replace('\t', ' _____ ')
                
                if not q_text:
                    q_text = "Chọn đáp án đúng nhất."
                
                # Clean choices
                cleaned_choices = []
                for c in current_choices:
                    c = c.replace('\t', ' ').strip()
                    cleaned_choices.append(c)
                
                problems.append({
                    "id": f"g7-english-{len(problems)+1}",
                    "topicId": "g7-english",
                    "question": q_text,
                    "choices": cleaned_choices,
                    "answer": current_answer,
                    "type": "multiple-choice" if cleaned_choices else "essay",
                    "steps": [{"text": "Dựa vào kiến thức đã học để trả lời.", "highlight": None}]
                })
            current_q = []
            current_choices = []
            current_answer = -1

        for line in group:
            text = line["text"]
            bold = line["bold_text"]
            
            # Is it an instruction?
            if text.isupper() or "Choose the" in text or "Read the following" in text:
                if current_q or current_choices:
                    save()
                instruction.append(text)
                continue
                
            # Is it a question start?
            if re.match(r'^(Question|Câu)\s*\d+.*', text, re.I):
                save()
                current_q.append(text)
                continue
                
            # Is it choices?
            # Check if it contains A. B. C. D. or \t indicating split choices
            if re.search(r'\b[A-D][\.\)]\s+', text) or (current_q and '\t' in text and len(current_choices) < 4):
                # It's a choice line!
                
                # Custom split for missing A. B.
                # E.g. "the same as in the past\tC. lower now than in the past"
                parts = re.split(r'(?=\b[A-D][\.\)]\s+)', text)
                if len(parts) == 1 and '\t' in text:
                    # just split by \t
                    parts = text.split('\t')
                
                for p in parts:
                    p = p.strip()
                    if not p: continue
                    # Add A. B. C. D. if missing
                    idx = len(current_choices)
                    prefix = ["A. ", "B. ", "C. ", "D. "]
                    
                    if not re.match(r'^[A-D][\.\)]', p) and idx < 4:
                        p = prefix[idx] + p
                        
                    current_choices.append(p)
                    
                    # Check answer
                    if bold:
                        # If the bold text is in this choice, or this choice is in bold text
                        # Remove A. B. C. D. for comparison
                        clean_p = re.sub(r'^[A-D][\.\)]\s*', '', p).strip()
                        clean_bold = re.sub(r'^[A-D][\.\)]\s*', '', bold).strip()
                        
                        if clean_bold and (clean_bold in clean_p or clean_p in clean_bold):
                            current_answer = len(current_choices) - 1
                
                continue
                
            # If not instruction, not question start, not choices, it's either continuation of question or a choice without A. B.
            if not current_choices:
                current_q.append(text)
            else:
                if len(current_choices) < 4:
                    idx = len(current_choices)
                    prefix = ["A. ", "B. ", "C. ", "D. "]
                    p = prefix[idx] + text
                    current_choices.append(p)
                    
                    clean_p = text.strip()
                    clean_bold = re.sub(r'^[A-D][\.\)]\s*', '', bold).strip()
                    if clean_bold and (clean_bold in clean_p or clean_p in clean_bold):
                        current_answer = len(current_choices) - 1
                else:
                    save()
                    current_q.append(text)
                
        save()
        
    print(f"Generated {len(problems)} problems")
    
    with open(r"E:\toanvui-main\scratch\english_problems.json", "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)

process()
