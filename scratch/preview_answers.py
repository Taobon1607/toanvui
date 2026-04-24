import docx2txt
import os

files_dir = r"d:\toanvui-main\toanvui-main\Đáp án đề cương"

print("--- TiengAnh7_DapAn.docx ---")
text_en = docx2txt.process(os.path.join(files_dir, "TiengAnh7_DapAn.docx"))
print(text_en[:500])

print("\n--- Toan7_DapAn.docx ---")
text_toan = docx2txt.process(os.path.join(files_dir, "Toan7_DapAn.docx"))
print(text_toan[:500])
