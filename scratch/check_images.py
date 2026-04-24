import json
import os

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

math_imgs = 0
en_imgs = 0
missing_files = []

for k, v in problems.items():
    if k.startswith("g7-math") and v.get("images"):
        math_imgs += len(v["images"])
        for img in v["images"]:
            filepath = os.path.join(r"d:\toanvui-main\toanvui-main\public", img.lstrip("/"))
            if not os.path.exists(filepath):
                missing_files.append(filepath)
                
    if k.startswith("g7-english") and v.get("images"):
        en_imgs += len(v["images"])

print(f"Total images attached to Math questions: {math_imgs}")
print(f"Total images attached to English questions: {en_imgs}")
print(f"Missing image files on disk: {len(missing_files)}")
