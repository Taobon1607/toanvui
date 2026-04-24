import json
import re

# 1. Update problems.js
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

# Insert before the last "};"
if problems_content.endswith("};\n"):
    problems_content = problems_content[:-3] + ",\n" + new_problems_js.rstrip(",\n") + "\n};\n"
else:
    problems_content = problems_content.rstrip()
    if problems_content.endswith("}"):
        problems_content = problems_content[:-1] + ",\n" + new_problems_js.rstrip(",\n") + "\n}"
    if problems_content.endswith(";"):
        problems_content += ";"

with open(problems_file, "w", encoding="utf-8") as f:
    f.write(problems_content)

print(f"Added {len(all_new_problems)} new problems to problems.js")

# 2. Update topics.js
topics_file = r"d:\toanvui-main\toanvui-main\src\data\topics.js"
with open(topics_file, "r", encoding="utf-8") as f:
    topics_content = f.read()

# We need to add the new topics to the "7" array.
# The IDs we generated are: g7-congnghe, g7-gdcd, g7-lichsu, g7-tin, g7-english, g7-math
new_topics = [
    {
      "id": "g7-congnghe",
      "gradeId": 7,
      "subject": "Công Nghệ",
      "name": "Ôn tập Công Nghệ",
      "emoji": "🛠️",
      "color": "#e67e22",
      "problemIds": list(docx_problems.keys())[0:41] # Filter ids by prefix
    },
    {
      "id": "g7-gdcd",
      "gradeId": 7,
      "subject": "GDCD",
      "name": "Ôn tập GDCD",
      "emoji": "🤝",
      "color": "#3498db",
      "problemIds": [k for k in docx_problems.keys() if k.startswith("g7-gdcd")]
    },
    {
      "id": "g7-lichsu",
      "gradeId": 7,
      "subject": "Lịch Sử & Địa Lý",
      "name": "Ôn tập Lịch Sử & Địa Lý",
      "emoji": "🌍",
      "color": "#16a085",
      "problemIds": [k for k in docx_problems.keys() if k.startswith("g7-lichsu")]
    },
    {
      "id": "g7-tin",
      "gradeId": 7,
      "subject": "Tin học",
      "name": "Ôn tập Tin học",
      "emoji": "💻",
      "color": "#9b59b6",
      "problemIds": [k for k in docx_problems.keys() if k.startswith("g7-tin")]
    },
    {
      "id": "g7-english",
      "gradeId": 7,
      "subject": "Tiếng Anh",
      "name": "Ôn tập Tiếng Anh",
      "emoji": "🇬🇧",
      "color": "#e74c3c",
      "problemIds": [k for k in pdf_problems.keys() if k.startswith("g7-english")]
    },
    {
      "id": "g7-math-new",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Đề cương ôn thi cuối kì Toán",
      "emoji": "📘",
      "color": "#f1c40f",
      "problemIds": [k for k in pdf_problems.keys() if k.startswith("g7-math")]
    }
]

# Quick fix for cong nghe
new_topics[0]["problemIds"] = [k for k in docx_problems.keys() if k.startswith("g7-congnghe")]

new_topics_js = ",\n".join([json.dumps(t, ensure_ascii=False, indent=4) for t in new_topics])

# Find the end of the "7": [ array
# Replace "g7-van-d2" block's end with a comma, then add the new_topics_js
pattern = r'("id": "g7-van-d2"[^}]+})'
replacement = r'\1,\n' + new_topics_js

updated_topics = re.sub(pattern, replacement, topics_content)

with open(topics_file, "w", encoding="utf-8") as f:
    f.write(updated_topics)

print("Updated topics.js with 6 new subjects.")
