import json
import re

# Load new problems
with open(r"d:\toanvui-main\toanvui-main\scratch\docx_problems.json", "r", encoding="utf-8") as f:
    docx_problems = json.load(f)

with open(r"d:\toanvui-main\toanvui-main\scratch\pdf_problems.json", "r", encoding="utf-8") as f:
    pdf_problems = json.load(f)

all_new_problems = {**docx_problems, **pdf_problems}

new_problems_js = ""
for key, value in all_new_problems.items():
    new_problems_js += f'  "{key}": {json.dumps(value, ensure_ascii=False, indent=2)},\n'

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    problems_content = f.read()

# Remove trailing semicolons and whitespaces, and the last closing brace
content_cleaned = problems_content.rstrip(" ;\n")
if content_cleaned.endswith("}"):
    content_cleaned = content_cleaned[:-1] # remove the last '}'
    # Now append the new data
    final_content = content_cleaned + ",\n" + new_problems_js.rstrip(",\n") + "\n};\n"
    
    with open(problems_file, "w", encoding="utf-8") as f:
        f.write(final_content)
    print(f"Successfully appended {len(all_new_problems)} problems.")
else:
    print("Could not find the end of the JSON object.")
