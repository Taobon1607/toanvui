import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

doc = Document(r'E:\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.docx')
paras = doc.paragraphs
# First 40 paras to see phonetics/stress
for i, para in enumerate(paras[:60]):
    text = para.text.strip()
    if not text:
        print(f"  [{i}] <BLANK>")
    else:
        bold_text = "".join(r.text for r in para.runs if r.bold).strip()
        print(f"  [{i}] text={repr(text[:110])}")
        print(f"        bold={repr(bold_text[:80])}")
