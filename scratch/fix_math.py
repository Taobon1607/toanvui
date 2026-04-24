import json
import re

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace the whole block for g7-math-13
pattern = r'("g7-math-13": \{[\s\S]*?\n\s*\})'

replacement = '''"g7-math-13": {
  "id": "g7-math-13",
  "topicId": "g7-math",
  "question": "Biểu thức đại số biểu thị cho tổng các bình phương của x và y là:",
  "choices": [
    "x² + y²",
    "(x + y)²",
    "x² + y",
    "x + y²"
  ],
  "answer": 0,
  "steps": [
    {
      "text": "Đáp án: A. x² + y²",
      "highlight": null
    }
  ],
  "images": [],
  "type": "mcq"
}'''

updated_content = re.sub(pattern, replacement, content)

with open(problems_file, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Fixed g7-math-13.")
