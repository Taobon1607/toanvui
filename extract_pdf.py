import fitz
import sys
import json

def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(min(50, len(doc))): # Extract max 50 pages for overview
        page = doc.load_page(page_num)
        text += page.get_text()
    return text

files = [
    "tai-lieu-hoc-tap-mon-toan-7-hoc-ki-1-nam-hoc-2025-2026.pdf",
    "tai-lieu-hoc-them-mon-toan-7-sach-canh-dieu-hoc-ki-1.pdf",
    "tai-lieu-hoc-them-mon-toan-7-sach-canh-dieu-hoc-ki-2.pdf",
    "tom-tat-ly-thuyet-va-cac-dang-bai-tap-quan-he-giua-cac-yeu-to-trong-mot-tam-giac.pdf"
]

results = {}
for f in files:
    try:
        results[f] = extract_text(f)
    except Exception as e:
        results[f] = f"Error: {e}"

print(json.dumps(results, indent=2))
