import fitz
import json

def extract_text(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page_num in range(min(30, len(doc))): # Extract max 30 pages
            page = doc.load_page(page_num)
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error: {e}"

files = [
    "tai-lieu-hoc-tap-mon-toan-7-hoc-ki-1-nam-hoc-2025-2026.pdf",
    "tai-lieu-hoc-them-mon-toan-7-sach-canh-dieu-hoc-ki-1.pdf",
    "tai-lieu-hoc-them-mon-toan-7-sach-canh-dieu-hoc-ki-2.pdf",
    "tom-tat-ly-thuyet-va-cac-dang-bai-tap-quan-he-giua-cac-yeu-to-trong-mot-tam-giac.pdf"
]

results = {}
for f in files:
    results[f] = extract_text(f)

with open("pdf_overview.json", "w", encoding="utf-8") as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
