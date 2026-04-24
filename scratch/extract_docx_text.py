import zipfile
import xml.etree.ElementTree as ET
import os

def extract_text_from_docx(docx_path):
    try:
        with zipfile.ZipFile(docx_path, 'r') as zip_ref:
            xml_content = zip_ref.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            texts = []
            for paragraph in tree.findall('.//w:p', ns):
                for run in paragraph.findall('.//w:r', ns):
                    for text in run.findall('.//w:t', ns):
                        texts.append(text.text)
                texts.append('\n')
            return ''.join(texts)
    except Exception as e:
        return f"Error: {e}"

files = ["Đề Cương KHTN 7.docx", "Đề Cương Ngữ Văn 7A10.docx"]
output_path = os.path.join(r"d:\toanvui-main\toanvui-main\scratch", "extracted_text.txt")
os.makedirs(os.path.dirname(output_path), exist_ok=True)

with open(output_path, "w", encoding="utf-8") as out:
    for f in files:
        path = os.path.join(r"d:\toanvui-main\toanvui-main", f)
        out.write(f"--- CONTENT OF {f} ---\n")
        content = extract_text_from_docx(path)
        out.write(content)
        out.write("\n" + "-" * 50 + "\n")
