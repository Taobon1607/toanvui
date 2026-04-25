import json
import os

problems_js_path = r"E:\toanvui-main\src\data\problems.js"
topics_js_path = r"E:\toanvui-main\src\data\topics.js"
parsed_english_path = r"E:\toanvui-main\scratch\english_parsed_v3.json"

# 1. Read the newly parsed english problems
with open(parsed_english_path, "r", encoding="utf-8") as f:
    english_problems = json.load(f)

# 2. Update problems.js
with open(problems_js_path, "r", encoding="utf-8") as f:
    content = f.read()

# Need to be careful with rstrip - problems.js might end with };\n
json_str = content.replace("export const problems = ", "").strip()
if json_str.endswith(";"):
    json_str = json_str[:-1]

data = json.loads(json_str)

# Remove all existing g7-english- problems
keys_to_delete = [k for k in data.keys() if k.startswith("g7-english-")]
for k in keys_to_delete:
    del data[k]

# Add new english problems
for p in english_problems:
    data[p["id"]] = p

# Write back problems.js
with open(problems_js_path, "w", encoding="utf-8") as f:
    f.write("export const problems = ")
    json.dump(data, f, ensure_ascii=False, indent=2)
    f.write(";\n")
print(f"Updated problems.js. Removed {len(keys_to_delete)} and added {len(english_problems)} english problems.")

# 3. Update topics.js
with open(topics_js_path, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content.replace("export const topics = ", "").strip()
if json_str.endswith(";"):
    json_str = json_str[:-1]
    
topics_data = json.loads(json_str)

# Find g7-english in grade 7
if "7" in topics_data:
    for topic in topics_data["7"]:
        if topic["id"] == "g7-english":
            topic["problemIds"] = [p["id"] for p in english_problems]
            break

# Write back topics.js
with open(topics_js_path, "w", encoding="utf-8") as f:
    f.write("export const topics = ")
    json.dump(topics_data, f, ensure_ascii=False, indent=2)
    f.write(";\n")
print(f"Updated topics.js with {len(english_problems)} problem IDs for g7-english.")
