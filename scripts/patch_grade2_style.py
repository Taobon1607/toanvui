"""
Vá bổ sung gradeId/emoji/color cho các chủ đề Lớp 2 (đã bị thiếu khi tái cấu trúc trước đó).
Không đụng tới problems.js hay problemIds - chỉ thêm thuộc tính hiển thị.
"""
import json
import re

TOPIC_STYLE = {
    "g2-numbers100":  {"emoji": "🔢", "color": "#54A0FF"},
    "g2-addsub100":   {"emoji": "➕", "color": "#FF6B6B"},
    "g2-geomeasure":  {"emoji": "📏", "color": "#00B894"},
    "g2-wordproblem": {"emoji": "📖", "color": "#FF9F43"},
    "g2-clockstats":  {"emoji": "🕒", "color": "#FFD32A"},
    "g2-muldiv25":    {"emoji": "✖️", "color": "#5F27CD"},
    "g2-numbers1000": {"emoji": "💯", "color": "#00CEC9"},
    "g2-addsub1000":  {"emoji": "➖", "color": "#FF6B6B"},
    "g2-measureadv":  {"emoji": "⚖️", "color": "#FF9F43"},
    "g2-wordmuldiv":  {"emoji": "🧩", "color": "#5F27CD"},
    "g2-midterm":     {"emoji": "📝", "color": "#FF6B6B"},
    "g2-final":       {"emoji": "🎓", "color": "#00B894"},
}


def main():
    with open('src/data/topics.js', 'r', encoding='utf-8') as f:
        topics = json.loads(re.search(r'export const topics = (\{[\s\S]*?\});', f.read()).group(1))

    patched = 0
    for t in topics.get('2', []):
        style = TOPIC_STYLE.get(t['id'])
        if not style:
            print(f"CẢNH BÁO: không có style định nghĩa cho '{t['id']}', bỏ qua.")
            continue
        t['gradeId'] = 2
        t['emoji'] = style['emoji']
        t['color'] = style['color']
        patched += 1

    with open('src/data/topics.js', 'w', encoding='utf-8') as f:
        f.write(f"export const topics = {json.dumps(topics, ensure_ascii=False, indent=2)};\n")

    print(f"Đã vá {patched}/{len(topics.get('2', []))} chủ đề Lớp 2 với gradeId/emoji/color.")


if __name__ == '__main__':
    main()
