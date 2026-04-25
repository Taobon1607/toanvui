import json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

s = open(r'E:\toanvui-main\src\data\topics.js', encoding='utf-8').read()
s = s.replace('export const topics = ', '').rstrip(';\n ')
d = json.loads(s)
for t in d.get('7', []):
    print(t['id'], '|', t.get('subject',''), '|', t.get('name',''))
