import sys, io, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def has_any_marker(text):
    return bool(re.search(r'(?:^|\s)[A-D][\.\)]\s*', text))

texts = [
    'C. =13+14+15\t\t\t\tD. =30+19*2',
    'A. 2. B. 3. C. 4. D. 5.',
    'Emphasis \tB. Motion Paths',
    'dãy số A.'
]

for t in texts:
    print(f"'{t}': {has_any_marker(t)}")

def is_question_start(text):
    # Old regex
    # return bool(re.match(r'^(?:Câu|Question|Q|(\d+))\s*\d*[\.\:\)]\s*', text, re.I))
    # New regex
    return bool(re.match(r'^(?:Câu|Question|Q)\s*\d+[\.\:\)]\s*', text, re.I))

print(f"'2.': {is_question_start('2.')}")
print(f"'Câu 22:': {is_question_start('Câu 22:')}")
