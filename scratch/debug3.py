import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

doc = Document(r'E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx')
paras = doc.paragraphs
# Find câu 50 (around index 170-200)
for i, para in enumerate(paras[155:]):
    real_i = i + 155
    text = para.text.strip()
    if not text:
        print(f"  [{real_i}] <BLANK>")
    else:
        bold_text = "".join(r.text for r in para.runs if r.bold).strip()
        print(f"  [{real_i}] text={repr(text[:100])}")
        print(f"        bold={repr(bold_text[:80])}")
    if real_i > 185:
        break
