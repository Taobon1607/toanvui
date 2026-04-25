import json
import re
from docx import Document

def parse_docx_to_problems(filepath, output_path):
    doc = Document(filepath)
    problems = []
    
    current_instruction = ""
    pending_text = []
    
    def clean_text(text):
        return text.strip().replace('\t', ' ').replace('\n', ' ')

    def save_problem(q_text, choices, answer_idx):
        if not choices:
            return
        
        # If question text is just a number like "1.", try to prepend instruction
        if re.match(r'^\d+[\.\)]\s*$', q_text) or not q_text:
            q_text = current_instruction + " " + q_text
            
        problems.append({
            "id": f"g7-english-{len(problems)+1}",
            "topicId": "g7-english",
            "question": q_text.strip(),
            "choices": choices,
            "answer": answer_idx,
            "type": "multiple-choice"
        })

    current_question = None
    marker_regex = r'\b([A-D][\.\)])'

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
            
        if text.isupper() or text.startswith("Choose the word") or text.startswith("Choose the best"):
            if current_question:
                save_problem(current_question["q"], current_question["choices"], current_question["answer"])
                current_question = None
            current_instruction = text
            pending_text = []
            continue

        runs_data = [{"text": r.text, "bold": r.bold} for r in para.runs if r.text]
        has_markers = re.search(marker_regex, text)
        
        if has_markers:
            choices_in_para = []
            curr_c = {"text": "", "bold": False}
            for run in runs_data:
                parts = re.split(marker_regex, run["text"])
                for i, part in enumerate(parts):
                    if i % 2 == 1:
                        if curr_c["text"].strip():
                            choices_in_para.append(curr_c)
                        curr_c = {"text": part, "bold": run["bold"]}
                    else:
                        curr_c["text"] += part
                        if run["bold"]: curr_c["bold"] = True
            if curr_c["text"].strip():
                choices_in_para.append(curr_c)
            
            cleaned_choices = []
            ans_in_para = -1
            for i, c in enumerate(choices_in_para):
                t = clean_text(c["text"])
                clean_t = re.sub(r'^[A-D][\.\)]\s*', '', t)
                cleaned_choices.append(clean_t)
                if c["bold"]: ans_in_para = i

            first_marker = re.search(marker_regex, text).group(1)[0]
            
            if current_question and first_marker != 'A':
                start_idx = len(current_question["choices"])
                current_question["choices"].extend(cleaned_choices)
                if ans_in_para != -1:
                    current_question["answer"] = start_idx + ans_in_para
            else:
                if current_question:
                    save_problem(current_question["q"], current_question["choices"], current_question["answer"])
                
                q_text = " ".join(pending_text) if pending_text else ""
                current_question = {
                    "q": q_text,
                    "choices": cleaned_choices,
                    "answer": ans_in_para if ans_in_para != -1 else 0
                }
                pending_text = []
        else:
            if current_question:
                save_problem(current_question["q"], current_question["choices"], current_question["answer"])
                current_question = None
            pending_text.append(text)

    if current_question:
        save_problem(current_question["q"], current_question["choices"], current_question["answer"])

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(problems, f, ensure_ascii=False, indent=2)
    print(f"Parsed {len(problems)} problems to {output_path}")

if __name__ == "__main__":
    filepath = r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx"
    output_path = r"E:\toanvui-main\scratch\g7-english_parsed_v4.json"
    parse_docx_to_problems(filepath, output_path)
