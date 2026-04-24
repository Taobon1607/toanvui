import os
import docx2txt
from pypdf import PdfReader

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"

files_to_check = [
    "Công Nghệ.docx",
    "GDCD.docx",
    "Lịch Sử Địa Lý.docx",
    "Tin học.docx",
    "Tiếng Anh.pdf",
    "Toán.pdf"
]

for filename in files_to_check:
    filepath = os.path.join(files_dir, filename)
    print(f"\n--- {filename} ---")
    if filename.endswith(".docx"):
        try:
            text = docx2txt.process(filepath)
            print(text[:500] + "\n...")
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
    elif filename.endswith(".pdf"):
        try:
            reader = PdfReader(filepath)
            text = ""
            for i in range(min(2, len(reader.pages))):
                text += reader.pages[i].extract_text() + "\n"
            print(text[:500] + "\n...")
        except Exception as e:
            print(f"Error parsing PDF: {e}")

