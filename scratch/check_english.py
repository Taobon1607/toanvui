import fitz
doc = fitz.open(r"d:\toanvui-main\toanvui-main\Đề cương ôn thi lớp 7\Tiếng Anh.pdf")
text = ""
for i in range(1, min(4, len(doc))):
    text += doc[i].get_text()
print(text[:1500])
