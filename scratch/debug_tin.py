import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

doc = Document(r'E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx')

for i, para in enumerate(doc.paragraphs[:60]):
    text = para.text.strip()
    if not text:
        print(f"  [{i}] <BLANK>")
    else:
        bold_text = "".join(r.text for r in para.runs if r.bold).strip()
        print(f"  [{i}] text={repr(text[:80])} bold={repr(bold_text[:50])}")
