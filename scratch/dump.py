import json
import re

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

with open(r"d:\toanvui-main\toanvui-main\scratch\dump_questions.txt", "w", encoding="utf-8") as f:
    f.write("--- ENGLISH ---\n")
    for k, v in problems.items():
        if k.startswith("g7-english"):
            f.write(f"[{k}] {v['question'][:100]}\n")
            if v.get("choices"):
                f.write(f"  Choices: {v['choices']}\n")
    
    f.write("\n--- MATH ---\n")
    for k, v in problems.items():
        if k.startswith("g7-math"):
            f.write(f"[{k}] {v['question'][:100]}\n")
            if v.get("choices"):
                f.write(f"  Choices: {v['choices']}\n")
