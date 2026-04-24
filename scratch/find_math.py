import json

problems_file = r"d:\toanvui-main\toanvui-main\src\data\problems.js"
with open(problems_file, "r", encoding="utf-8") as f:
    content = f.read()

json_str = content[content.find("{"):content.rfind("}")+1]
problems = json.loads(json_str)

for k, v in problems.items():
    if k.startswith("g7-math"):
        if "bình phương" in v["question"]:
            print(f"FOUND MATCH ID: {k}")
            print(json.dumps(v, ensure_ascii=False, indent=2))
