import json

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

import re
# We want to replace the step text for g7-english-126
# "Almost all our energy/ come/ oil/ gas/ natural gas."
pattern = r'("id": "g7-english-126"[\s\S]*?"steps": \[\s*\{\s*"text": )"Dựa vào kiến thức đã học để trả lời\."'
replacement = r'\1"Almost all our energy comes from oil, gas, and natural gas."'

updated_content = re.sub(pattern, replacement, content)

with open(problems_file, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Updated answer for g7-english-126.")
