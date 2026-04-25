import json
import re
import os

def update_problems_js(problems_json_path, problems_js_path):
    with open(problems_json_path, 'r', encoding='utf-8') as f:
        new_problems_list = json.load(f)
    
    new_problems_dict = {p['id']: p for p in new_problems_list}
    
    with open(problems_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the object content
    match = re.search(r'export const problems = (\{.*?\});', content, re.DOTALL)
    if not match:
        # Try without semicolon
        match = re.search(r'export const problems = (\{.*?\})', content, re.DOTALL)
        
    if match:
        # This is dangerous if there are nested braces, but for this structure it might work
        # Better: find the last '};'
        start_idx = content.find('{')
        end_idx = content.rfind('};')
        if end_idx == -1: end_idx = content.rfind('}')
        
        # Actually, let's just append to the existing object before the last '};'
        # We'll just generate the new entries as strings
        new_entries = []
        for pid, pdata in new_problems_dict.items():
            new_entries.append(f'  "{pid}": {json.dumps(pdata, ensure_ascii=False, indent=2)}')
        
        insertion_text = ",\n" + ",\n".join(new_entries)
        
        # Find the last closing brace of the main object
        last_brace = content.rfind('}')
        new_content = content[:last_brace] + insertion_text + "\n" + content[last_brace:]
        
        with open(problems_js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {problems_js_path} with {len(new_problems_dict)} problems")
    else:
        print("Could not find problems object in JS file")

def update_topics_js(problems_json_path, topics_js_path):
    with open(problems_json_path, 'r', encoding='utf-8') as f:
        new_problems_list = json.load(f)
    
    problem_ids = [p['id'] for p in new_problems_list]
    
    with open(topics_js_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if '"id": "g7-english"' in content:
        print("Topic g7-english already exists, updating problem IDs")
        # Find the problemIds array for g7-english
        # We look for "id": "g7-english" and then the next "problemIds": [
        start_search = content.find('"id": "g7-english"')
        ids_start = content.find('"problemIds": [', start_search)
        ids_end = content.find(']', ids_start) + 1
        
        new_ids_json = json.dumps(problem_ids, indent=10).replace('[', '').replace(']', '').strip()
        new_ids_block = '"problemIds": [\n          ' + new_ids_json.replace('\n', '\n          ') + '\n        ]'
        
        new_content = content[:ids_start] + new_ids_block + content[ids_end:]
        with open(topics_js_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    else:
        print("Adding new topic g7-english")
        new_topic = {
            "id": "g7-english",
            "gradeId": 7,
            "subject": "Tiếng Anh",
            "name": "Đề Cương Ôn Tập",
            "emoji": "🇬🇧",
            "color": "#3498DB",
            "problemIds": problem_ids
        }
        
        target = '"7": ['
        idx = content.find(target)
        if idx != -1:
            insertion_point = idx + len(target)
            # Indent manually to match file style
            topic_json = json.dumps(new_topic, ensure_ascii=False, indent=6)
            new_topic_str = "\n    " + topic_json + ","
            new_content = content[:insertion_point] + new_topic_str + content[insertion_point:]
            
            with open(topics_js_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Added g7-english to {topics_js_path}")
        else:
            print("Could not find grade 7 in topics.js")

if __name__ == "__main__":
    p_json = r"E:\toanvui-main\scratch\g7-english_parsed_v4.json"
    p_js = r"E:\toanvui-main\src\data\problems.js"
    t_js = r"E:\toanvui-main\src\data\topics.js"
    
    update_problems_js(p_json, p_js)
    update_topics_js(p_json, t_js)
