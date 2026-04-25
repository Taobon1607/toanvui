import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from docx import Document

def debug_paras(filepath, start=0, end=80):
    doc = Document(filepath)
    for i, para in enumerate(doc.paragraphs[start:end], start=start):
        text = para.text.strip()
        if not text:
            print(f"  [{i}] <BLANK>")
        else:
            bold_text = "".join(r.text for r in para.runs if r.bold).strip()
            print(f"  [{i}] text={repr(text[:100])}")
            print(f"        bold={repr(bold_text[:80])}")

print("=== TIN HỌC (câu 22, câu 50) ===")
debug_paras(r"E:\toanvui-main\Đề cương ôn thi lớp 7\Tin học.docx", start=55, end=120)
