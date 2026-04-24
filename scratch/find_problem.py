import json

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

# Extract just the JSON part
json_str = content[content.find("{"):content.rfind("}")+1]

try:
    problems = json.loads(json_str)
    for k, v in problems.items():
        if "Almost all our energy" in v.get("question", ""):
            print(f"FOUND MATCH ID: {k}")
            print(json.dumps(v, ensure_ascii=False, indent=2))
except Exception as e:
    print("Error:", e)
