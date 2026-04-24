import json

# Read the generated problems
with open(r"d:\toanvui-main\toanvui-main\scratch\problems_gen.json", "r", encoding="utf-8") as f:
    new_problems = json.load(f)

# Convert to JS format (roughly)
new_problems_js = ""
for key, value in new_problems.items():
    new_problems_js += f'  "{key}": {json.dumps(value, ensure_ascii=False, indent=2)},\n'

# Read original file
with open(r"d:\toanvui-main\toanvui-main\src\data\problems.js", "r", encoding="utf-8") as f:
    lines = f.readlines()

# Find the point where my previous edits started
# Previous edit started at "g7-khtn-1"
start_idx = -1
for i, line in enumerate(lines):
    if '"g7-khtn-1": {' in line:
        start_idx = i
        break

if start_idx != -1:
    # Keep everything before g7-khtn-1
    # Note: I need to handle the last comma of the previous object if I'm not careful.
    # The line before g7-khtn-1 is "  }," (closing for the previous one)
    # The new_problems_js will be appended. 
    # BUT I need to remove the trailing comma and add the closing "};"
    
    new_content = "".join(lines[:start_idx]) + new_problems_js.rstrip(",\n") + "\n};"
    
    with open(r"d:\toanvui-main\toanvui-main\src\data\problems.js", "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Successfully updated problems.js with", len(new_problems), "problems.")
else:
    print("Could not find insertion point!")
