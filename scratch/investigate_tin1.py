import sys, io, re
from docx import Document

doc = Document(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx")
p1 = doc.paragraphs[1].text
print(f"TEXT: [{p1[:20]}]")
for i, c in enumerate(p1[:10]):
    print(f"Char {i}: [{c}] {hex(ord(c))}")

def has_choice_marker(text):
    return bool(re.search(r'(?:^|\s)[A-D][\.\)]', text))

print(f"Regex match: {has_choice_marker(p1)}")
print(f"Regex search: {re.search(r'(?:^|\s)[A-D][\.\)]', p1)}")
