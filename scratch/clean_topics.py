import json

# Define the full Grade 7 topics data structure
g7_topics = [
    {
      "id": "g7-rational",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Số Hữu Tỉ",
      "emoji": "",
      "color": "#F39C12",
      "problemIds": [
        "g7-rat-1", "g7-rat-2", "g7-rat-3", "g7-rat-4", "g7-rat-5", "g7-rat-6", "g7-rat-7", "g7-rat-8", "g7-rat-9", "g7-rat-10"
      ]
    },
    {
      "id": "g7-real",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Số Thực",
      "emoji": "",
      "color": "#E67E22",
      "problemIds": [
        "g7-real-1", "g7-real-2", "g7-real-3", "g7-real-4", "g7-real-5", "g7-real-6", "g7-real-7", "g7-real-8", "g7-real-9", "g7-real-10"
      ]
    },
    {
      "id": "g7-geometry-3d",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Hình học trực quan 3D",
      "emoji": "📦",
      "color": "#D35400",
      "problemIds": [
        "g7-geo3d-1", "g7-geo3d-2", "g7-geo3d-3", "g7-geo3d-4", "g7-geo3d-5", "g7-geo3d-6", "g7-geo3d-7", "g7-geo3d-8", "g7-geo3d-9", "g7-geo3d-10"
      ]
    },
    {
      "id": "g7-angles",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Góc & Đường song song",
      "emoji": "📐",
      "color": "#27AE60",
      "problemIds": [
        "g7-ang-1", "g7-ang-2", "g7-ang-3", "g7-ang-4", "g7-ang-5", "g7-ang-6", "g7-ang-7", "g7-ang-8", "g7-ang-9", "g7-ang-10"
      ]
    },
    {
      "id": "g7-triangle-congruence",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Tam giác bằng nhau",
      "emoji": "🔺",
      "color": "#16A085",
      "problemIds": [
        "g7-tri-1", "g7-tri-2", "g7-tri-3", "g7-tri-4", "g7-tri-5", "g7-tri-6", "g7-tri-7", "g7-tri-8", "g7-tri-9", "g7-tri-10",
        "g7-tri-11", "g7-tri-12", "g7-tri-13", "g7-tri-14", "g7-tri-15", "g7-tri-16", "g7-tri-17", "g7-tri-18", "g7-tri-19", "g7-tri-20",
        "g7-tri-21", "g7-tri-22", "g7-tri-23", "g7-tri-24", "g7-tri-25", "g7-tri-26", "g7-tri-27", "g7-tri-28", "g7-tri-29", "g7-tri-30",
        "g7-tri-31", "g7-tri-32", "g7-tri-33", "g7-tri-34", "g7-tri-35", "g7-tri-36", "g7-tri-37", "g7-tri-38", "g7-tri-39", "g7-tri-40",
        "g7-tri-41", "g7-tri-42", "g7-tri-43", "g7-tri-44", "g7-tri-45", "g7-tri-46", "g7-tri-47", "g7-tri-48", "g7-tri-49", "g7-tri-50"
      ]
    },
    {
      "id": "g7-exam-final",
      "gradeId": 7,
      "subject": "Toán Học",
      "name": "Ôn tập Tổng hợp Toán",
      "emoji": "🏆",
      "color": "#F1C40F",
      "problemIds": [
        "g7-exam-1", "g7-exam-2", "g7-exam-3", "g7-exam-4", "g7-exam-5", "g7-exam-6", "g7-exam-7", "g7-exam-8", "g7-exam-9", "g7-exam-10",
        "g7-exam-11", "g7-exam-12", "g7-exam-13", "g7-exam-14", "g7-exam-15", "g7-exam-16", "g7-exam-17", "g7-exam-18", "g7-exam-19", "g7-exam-20",
        "g7-exam-21", "g7-exam-22", "g7-exam-23", "g7-exam-24", "g7-exam-25", "g7-exam-26", "g7-exam-27", "g7-exam-28", "g7-exam-29", "g7-exam-30",
        "g7-exam-31", "g7-exam-32", "g7-exam-33", "g7-exam-34", "g7-exam-35", "g7-exam-36", "g7-exam-37", "g7-exam-38", "g7-exam-39", "g7-exam-40",
        "g7-exam-41", "g7-exam-42", "g7-exam-43", "g7-exam-44", "g7-exam-45", "g7-exam-46", "g7-exam-47", "g7-exam-48", "g7-exam-49", "g7-exam-50"
      ]
    },
    {
      "id": "g7-khtn-c1",
      "gradeId": 7,
      "subject": "Khoa Học Tự Nhiên",
      "name": "KHTN: Chất & Biến đổi",
      "emoji": "🧪",
      "color": "#00CEC9",
      "problemIds": [
        "g7-khtn-c1-1", "g7-khtn-c1-2", "g7-khtn-c1-3", "g7-khtn-c1-4", "g7-khtn-c1-5",
        "g7-khtn-c1-6", "g7-khtn-c1-7", "g7-khtn-c1-8", "g7-khtn-c1-9", "g7-khtn-c1-10",
        "g7-khtn-c1-11", "g7-khtn-c1-12", "g7-khtn-c1-tf1a", "g7-khtn-c1-tf1b", 
        "g7-khtn-c1-tf1c", "g7-khtn-c1-tf1d", "g7-khtn-c1-e1", "g7-khtn-c1-e2"
      ]
    },
    {
      "id": "g7-khtn-c2",
      "gradeId": 7,
      "subject": "Khoa Học Tự Nhiên",
      "name": "KHTN: Năng lượng",
      "emoji": "⚡",
      "color": "#FDCB6E",
      "problemIds": [
        "g7-khtn-c2-1", "g7-khtn-c2-2", "g7-khtn-c2-3", "g7-khtn-c2-4", "g7-khtn-c2-5",
        "g7-khtn-c2-6", "g7-khtn-c2-7", "g7-khtn-c2-8", "g7-khtn-c2-9", "g7-khtn-c2-10",
        "g7-khtn-c2-11", "g7-khtn-c2-12", "g7-khtn-c2-13", "g7-khtn-c2-14", "g7-khtn-c2-15"
      ]
    },
    {
      "id": "g7-khtn-c3",
      "gradeId": 7,
      "subject": "Khoa Học Tự Nhiên",
      "name": "KHTN: Vật sống",
      "emoji": "🌿",
      "color": "#00B894",
      "problemIds": [
        "g7-khtn-c3-1", "g7-khtn-c3-2", "g7-khtn-c3-3", "g7-khtn-c3-4", "g7-khtn-c3-5",
        "g7-khtn-c3-6", "g7-khtn-c3-15", "g7-khtn-c3-20"
      ]
    },
    {
      "id": "g7-van-d1",
      "gradeId": 7,
      "subject": "Ngữ Văn",
      "name": "Ngữ Văn: Đề minh họa 1",
      "emoji": "📝",
      "color": "#6C5CE7",
      "problemIds": [
        "g7-van-d1-1", "g7-van-d1-2", "g7-van-d1-3", "g7-van-d1-4", "g7-van-d1-6",
        "g7-van-d1-9", "g7-van-d1-11"
      ]
    },
    {
      "id": "g7-van-d2",
      "gradeId": 7,
      "subject": "Ngữ Văn",
      "name": "Ngữ Văn: Đề minh họa 2",
      "emoji": "📜",
      "color": "#A29BFE",
      "problemIds": [
        "g7-van-d2-1", "g7-van-d2-3", "g7-van-d2-6", "g7-van-d2-7", "g7-van-d2-8"
      ]
    }
]

file_path = r"d:\toanvui-main\toanvui-main\src\data\topics.js"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find the start and end of Grade 7 topics array
# Current messy state has "7": [ ... ];
import re
new_g7_str = '  "7": ' + json.dumps(g7_topics, ensure_ascii=False, indent=2) + "\n};"
pattern = r'  "7": \[\s*[\s\S]*' # Matches from "7": [ to end of file

updated_content = re.sub(pattern, new_g7_str, content)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Successfully cleaned up topics.js Grade 7 section.")
