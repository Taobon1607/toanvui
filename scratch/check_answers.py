import os
import fitz
import docx2txt

files_dir = r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7"

# Check PDF for answer keys (last 3 pages)
doc = fitz.open(os.path.join(files_dir, "Tiếng Anh.pdf"))
text = ""
for i in range(max(0, len(doc)-3), len(doc)):
    text += doc[i].get_text()
print("--- Tiếng Anh.pdf End ---")
print(text[-1000:])

doc = fitz.open(os.path.join(files_dir, "Toán.pdf"))
text = ""
for i in range(max(0, len(doc)-3), len(doc)):
    text += doc[i].get_text()
print("--- Toán.pdf End ---")
print(text[-1000:])

# Check DOCX for answer keys (last 1000 chars)
try:
    text = docx2txt.process(os.path.join(files_dir, "Tin học.docx"))
    print("--- Tin học.docx End ---")
    print(text[-1000:])
except: pass

try:
    text = docx2txt.process(os.path.join(files_dir, "GDCD.docx"))
    print("--- GDCD.docx End ---")
    print(text[-1000:])
except: pass
