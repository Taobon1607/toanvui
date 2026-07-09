"""
Tái cấu trúc chủ đề Lớp 2 theo SÁT chương trình SGK Toán 2 - Chân Trời Sáng Tạo.
- Xóa 8 chủ đề cũ (chung chung, không bám khung SGK).
- Dựng lại 12 chủ đề mới: 5 HK1 + 5 HK2 + Đề Giữa Kỳ + Đề Cuối Kỳ.
- DI TRÚ (giữ lại) các bài cũ còn phù hợp về nội dung/phạm vi, gắn lại topicId + id mới.
- Sinh bổ sung bài mới cho tới khi mỗi chủ đề đạt đủ TARGET bài.
"""
import json
import re
import random

random.seed(20702)

TARGET = 100

NAMES = ['Lan', 'Bình', 'Hoa', 'Huy', 'Minh', 'Tuấn', 'Mai', 'An', 'Nam', 'Trang', 'Linh', 'Phong', 'Hương', 'Đức', 'Vy', 'Hùng']
SCHOOL_ITEMS = ['quyển vở', 'cây bút', 'quyển sách', 'cái bánh', 'bông hoa', 'chiếc kẹo', 'quả bóng bay']
FRUITS = ['quả táo 🍎', 'quả cam 🍊', 'quả chuối 🍌', 'quả dâu 🍓', 'quả bưởi 🍈', 'quả lê 🍐', 'quả đào 🍑', 'quả quýt 🍊']
BOXES = ['hộp', 'rổ', 'giỏ', 'túi', 'thùng']
ANIMAL_PAIRS = [
    ('lợn', 'chó', 15, 60),
    ('trâu', 'bò', 150, 400),
    ('ngựa', 'dê', 80, 250),
    ('gà', 'vịt', 1, 4),
]
LIQUIDS = ['nước mắm', 'nước cam', 'sữa', 'dầu ăn', 'nước']
GOODS = ['gạo', 'đường', 'bột mì', 'muối', 'ngô']
SOLID_EXAMPLES = [
    ('lon nước ngọt', 'khối trụ'), ('hộp sữa hình ống', 'khối trụ'), ('cây cột nhà', 'khối trụ'),
    ('quả bóng đá', 'khối cầu'), ('viên bi', 'khối cầu'), ('quả địa cầu', 'khối cầu'),
    ('mặt bàn học', 'hình tứ giác'), ('ô cửa sổ', 'hình tứ giác'), ('viên gạch lát nền', 'hình tứ giác'),
]

# ===== Chống trùng lặp =====
generated_questions = set()

def is_duplicate(question_text):
    normalized = re.sub(r'\s+', ' ', question_text).strip().lower()
    if normalized in generated_questions:
        return True
    generated_questions.add(normalized)
    return False


def make_choices(correct_val, unit='', incorrect_offset=10, min_val=0):
    choices = [correct_val]
    attempts = 0
    while len(choices) < 4 and attempts < 200:
        attempts += 1
        offset = random.randint(-incorrect_offset, incorrect_offset)
        if offset == 0:
            continue
        val = correct_val + offset
        if val < min_val:
            continue
        if val not in choices:
            choices.append(val)
    str_choices = [f"{c}{unit}" for c in choices]
    random.shuffle(str_choices)
    correct_str = f"{correct_val}{unit}"
    ans_idx = str_choices.index(correct_str)
    return str_choices, ans_idx


NUM_WORDS_TENS = {2: 'hai mươi', 3: 'ba mươi', 4: 'bốn mươi', 5: 'năm mươi',
                  6: 'sáu mươi', 7: 'bảy mươi', 8: 'tám mươi', 9: 'chín mươi'}
NUM_WORDS_UNITS = {1: 'mốt', 2: 'hai', 3: 'ba', 4: 'tư', 5: 'lăm',
                   6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}

def number_to_words_2digit(n):
    tens, units = divmod(n, 10)
    if tens == 0:
        return {1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'}[units]
    if units == 0:
        return NUM_WORDS_TENS[tens]
    return f"{NUM_WORDS_TENS[tens]} {NUM_WORDS_UNITS[units]}"


# ==================================================================
# HK1 - 1. g2-numbers100 : Số Đến 100
# ==================================================================
def gen_numbers100(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6])
        if pattern == 1:
            n = random.randint(21, 99)
            words = number_to_words_2digit(n)
            q = f"Số \"{words.capitalize()}\" được viết là:"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(n, incorrect_offset=8, min_val=10)
            steps = [{"text": f"\"{words.capitalize()}\" viết bằng số là {n}. ✅", "highlight": None}]
        elif pattern == 2:
            n = random.randint(11, 98)
            asks_next = random.random() < 0.5
            if asks_next:
                q = f"Số liền sau của số {n} là:"
                ans_val = n + 1
                steps = [{"text": f"Số liền sau hơn số đã cho 1 đơn vị: {n} + 1 = {n + 1}. ✅", "highlight": None}]
            else:
                q = f"Số liền trước của số {n} là:"
                ans_val = n - 1
                steps = [{"text": f"Số liền trước kém số đã cho 1 đơn vị: {n} - 1 = {n - 1}. ✅", "highlight": None}]
            if is_duplicate(q):
                continue
            choices, ans = make_choices(ans_val, incorrect_offset=3, min_val=0)
        elif pattern == 3:
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            if a == b:
                continue
            q = f"So sánh: {a} ... {b}"
            if is_duplicate(q):
                continue
            correct = '<' if a < b else '>'
            choices = ['>', '<', '=', '?']
            ans = choices.index(correct)
            steps = [{"text": f"So sánh hàng chục trước, rồi đến hàng đơn vị. Vậy {a} {correct} {b}. ✅", "highlight": None}]
        elif pattern == 4:
            tens = random.randint(1, 9)
            units = random.randint(1, 9)
            n = tens * 10 + units
            q = f"Số {n} gồm mấy chục và mấy đơn vị?"
            if is_duplicate(q):
                continue
            correct = f"{tens} chục và {units} đơn vị"
            wrongs = set()
            while len(wrongs) < 3:
                wt = random.randint(1, 9)
                wu = random.randint(0, 9)
                w = f"{wt} chục và {wu} đơn vị"
                if w != correct:
                    wrongs.add(w)
            choices = [correct] + list(wrongs)
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"{n} = {tens}0 + {units}, tức {tens} chục và {units} đơn vị. ✅", "highlight": None}]
        elif pattern == 5:
            nums = sorted(random.sample(range(10, 99), 4))
            ascending = random.random() < 0.5
            correct_seq = nums if ascending else nums[::-1]
            correct = ', '.join(map(str, correct_seq))
            wrong1 = ', '.join(map(str, correct_seq[::-1]))
            shuffled = correct_seq[:]
            random.shuffle(shuffled)
            wrong2 = ', '.join(map(str, shuffled))
            wrong3 = ', '.join(map(str, sorted(random.sample(range(10, 99), 4))))
            direction = "bé đến lớn" if ascending else "lớn đến bé"
            q = f"Dãy số nào dưới đây được sắp xếp theo thứ tự từ {direction}: {', '.join(map(str, nums))}?"
            if is_duplicate(q):
                continue
            choices = list(dict.fromkeys([correct, wrong1, wrong2, wrong3]))
            while len(choices) < 4:
                choices.append(', '.join(map(str, random.sample(range(10, 99), 4))))
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Sắp xếp các số theo thứ tự từ {direction}: {correct}. ✅", "highlight": None}]
        else:
            tens = random.randint(1, 9) * 10
            units = random.randint(1, 9)
            total = tens + units
            ask_units = random.random() < 0.5
            if ask_units:
                q = f"{total} gồm {tens} và ...?"
                ans_val = units
            else:
                q = f"... gồm {tens} và {units}?"
                ans_val = total
            if is_duplicate(q):
                continue
            choices, ans = make_choices(ans_val, incorrect_offset=5, min_val=0)
            steps = [{"text": f"{total} = {tens} + {units}. ✅", "highlight": None}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK1 - 2. g2-addsub100 : Cộng Trừ Có Nhớ (Phạm Vi 100)
# ==================================================================
def gen_addsub100(pid, topic_id):
    while True:
        is_add = random.random() < 0.5
        if is_add:
            a = random.randint(15, 89)
            b = random.randint(15, 89)
            a_dv, b_dv = a % 10, b % 10
            if a_dv + b_dv < 10:
                b = min(b - b_dv + (10 - a_dv) if a_dv > 0 else b + 5, 89)
            total = a + b
            phrasing = random.choice([f"{a} + {b} = ?", f"Tính: {a} + {b} = ?", f"Đặt tính rồi tính: {a} + {b}"])
            q = phrasing
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=8, min_val=10)
            dv = a % 10 + b % 10
            steps = [
                {"text": f"Cộng hàng đơn vị: {a % 10} + {b % 10} = {dv}. Viết {dv % 10}, nhớ {dv // 10}.", "highlight": "co-nho"},
                {"text": f"Cộng hàng chục: {a // 10} + {b // 10} + {dv // 10}(nhớ) = {total // 10}.", "highlight": "co-nho"},
                {"text": f"Kết quả: {total} ✅", "highlight": None},
            ]
        else:
            a = random.randint(30, 95)
            b = random.randint(15, a - 5)
            a_dv, b_dv = a % 10, b % 10
            if a_dv >= b_dv:
                b = b + (a_dv - b_dv) + 1
                if b >= a:
                    b = a - 5
            diff = a - b
            if diff < 0:
                continue
            phrasing = random.choice([f"{a} - {b} = ?", f"Tìm M: M = {a} - {b}", f"Đặt tính rồi tính: {a} - {b} = ?"])
            q = phrasing
            if is_duplicate(q):
                continue
            choices, ans = make_choices(diff, incorrect_offset=8, min_val=0)
            a_dv2, b_dv2 = a % 10, b % 10
            steps = [
                {"text": f"Hàng đơn vị: {a_dv2} < {b_dv2} nên mượn 1 từ hàng chục. {a_dv2 + 10} - {b_dv2} = {a_dv2 + 10 - b_dv2}.", "highlight": "phep-tru"},
                {"text": f"Hàng chục: {a // 10} - 1(mượn) - {b // 10} = {diff // 10}.", "highlight": None},
                {"text": f"Kết quả: {diff} ✅", "highlight": None},
            ]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK1 - 3. g2-geomeasure : Hình Học & Đo Lường (cm, dm, lít)
# ==================================================================
def gen_geomeasure(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4])
        if pattern == 1:
            segs = [random.randint(1, 9) for _ in range(3)]
            total = sum(segs)
            labels = random.choice([('A', 'B', 'C', 'D'), ('M', 'N', 'P', 'Q')])
            q = (f"Tính độ dài đường gấp khúc {labels[0]}{labels[1]}{labels[2]}{labels[3]} có các đoạn thẳng: "
                 f"{labels[0]}{labels[1]} = {segs[0]}cm, {labels[1]}{labels[2]} = {segs[1]}cm, {labels[2]}{labels[3]} = {segs[2]}cm.")
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, unit=' cm', incorrect_offset=4, min_val=3)
            steps = [{"text": f"Độ dài đường gấp khúc = tổng độ dài các đoạn thẳng: {segs[0]} + {segs[1]} + {segs[2]} = {total} (cm). ✅", "highlight": None}]
        elif pattern == 2:
            dm = random.randint(1, 9)
            cm = dm * 10
            to_cm = random.random() < 0.5
            if to_cm:
                q = f"Đổi đơn vị: {dm} dm = ... cm"
                ans_val = cm
            else:
                q = f"Đổi đơn vị: {cm} cm = ... dm"
                ans_val = dm
            if is_duplicate(q):
                continue
            choices, ans = make_choices(ans_val, incorrect_offset=(5 if to_cm else 3), min_val=1)
            steps = [{"text": "Ta biết 1 dm = 10 cm.", "highlight": None}, {"text": f"Vậy kết quả là {ans_val}. ✅", "highlight": None}]
        elif pattern == 3:
            liquid = random.choice(LIQUIDS)
            parts = random.randint(2, 6)
            per = random.randint(2, 9)
            total = parts * per
            q = f"Có {total} lít {liquid} chia đều vào {parts} can. Mỗi can có bao nhiêu lít?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(per, unit=' lít', incorrect_offset=3, min_val=1)
            steps = [
                {"text": "Chia đều thì dùng phép chia.", "highlight": "phep-chia"},
                {"text": f"{total} ÷ {parts} = {per} (lít) ✅", "highlight": None},
            ]
        else:
            a = random.randint(2, 40)
            b = random.randint(2, 40)
            total = a + b
            q = f"Đoạn thẳng AB dài {a}cm, đoạn thẳng BC dài {b}cm. Nếu A, B, C thẳng hàng, đoạn thẳng AC dài bao nhiêu?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, unit=' cm', incorrect_offset=6, min_val=4)
            steps = [{"text": f"Vì A, B, C thẳng hàng nên AC = AB + BC = {a} + {b} = {total} (cm). ✅", "highlight": None}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK1 - 4. g2-wordproblem : Giải Toán Có Lời Văn (Nhiều Hơn - Ít Hơn)
# ==================================================================
def gen_wordproblem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3])
        item = random.choice(SCHOOL_ITEMS)
        class_a = random.choice(['2A', '2B', '2C', '1A', '3A'])
        class_b = random.choice([c for c in ['2A', '2B', '2C', '1A', '3A'] if c != class_a])

        if pattern == 1:
            base = random.randint(15, 70)
            more = random.randint(5, 30)
            total = base + more
            q = f"Lớp {class_a} quyên góp được {base} {item}. Lớp {class_b} quyên góp được nhiều hơn lớp {class_a} là {more} {item}. Hỏi lớp {class_b} quyên góp được bao nhiêu {item}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=10, min_val=5)
            steps = [
                {"text": "Bài toán \"nhiều hơn\" -> dùng phép cộng.", "highlight": "phep-cong"},
                {"text": f"{base} + {more} = {total} ({item}) ✅", "highlight": None},
            ]
        elif pattern == 2:
            base = random.randint(30, 90)
            less = random.randint(5, 25)
            total = base - less
            q = f"Bạn {random.choice(NAMES)} có {base} {item}. Bạn {random.choice(NAMES)} có ít hơn {less} {item}. Hỏi bạn đó có bao nhiêu {item}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=10, min_val=1)
            steps = [
                {"text": "Bài toán \"ít hơn\" -> dùng phép trừ.", "highlight": "phep-tru"},
                {"text": f"{base} - {less} = {total} ({item}) ✅", "highlight": None},
            ]
        else:
            have = random.randint(20, 80)
            add_or_sub = random.choice(['thêm', 'bớt'])
            change = random.randint(5, 20)
            name = random.choice(NAMES)
            if add_or_sub == 'thêm':
                total = have + change
                q = f"{name} có {have} {item}, mẹ cho {name} thêm {change} {item} nữa. Hỏi {name} có tất cả bao nhiêu {item}?"
                op_text = f"{have} + {change} = {total}"
                highlight = "phep-cong"
            else:
                total = have - change
                q = f"{name} có {have} {item}, {name} cho bạn {change} {item}. Hỏi {name} còn lại bao nhiêu {item}?"
                op_text = f"{have} - {change} = {total}"
                highlight = "phep-tru"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=10, min_val=1)
            steps = [
                {"text": f"Bài toán \"{add_or_sub}\" -> dùng phép {'cộng' if add_or_sub == 'thêm' else 'trừ'}.", "highlight": highlight},
                {"text": f"{op_text} ({item}) ✅", "highlight": None},
            ]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK1 - 5. g2-clockstats : Xem Giờ & Thống Kê Xác Suất
# ==================================================================
def gen_clockstats(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6])
        hour = random.randint(1, 11)

        if pattern == 1:
            q = f"Kim ngắn chỉ số {hour}, kim dài chỉ số 12. Đồng hồ đang chỉ mấy giờ?"
            if is_duplicate(q):
                continue
            correct = f"{hour} giờ"
            wrongs = [f"12 giờ", f"{hour + 1 if hour < 12 else 1} giờ", f"{hour} giờ 30 phút"]
            choices = list(dict.fromkeys([correct] + wrongs))
            while len(choices) < 4:
                w = f"{random.randint(1, 12)} giờ"
                if w not in choices:
                    choices.append(w)
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Kim ngắn chỉ số {hour} và kim dài chỉ số 12 -> đúng {hour} giờ. ✅", "highlight": "xem-gio"}]
        elif pattern == 2:
            n = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            minute = n * 5
            next_hour = hour + 1 if hour < 12 else 1
            q = f"Đồng hồ chỉ mấy giờ khi kim ngắn chỉ giữa số {hour} và số {next_hour}, kim dài chỉ số {n}?"
            if is_duplicate(q):
                continue
            correct = f"{hour} giờ {minute} phút" if minute != 0 else f"{hour} giờ"
            wrongs = set()
            while len(wrongs) < 3:
                w_n = random.choice([x for x in range(0, 12) if x != n])
                w = f"{hour} giờ {w_n * 5} phút" if w_n != 0 else f"{hour} giờ"
                if w != correct:
                    wrongs.add(w)
            choices = [correct] + list(wrongs)
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Kim dài chỉ số {n} tương ứng {minute} phút. Vậy là {correct}. ✅", "highlight": "kim-dong-ho"}]
        elif pattern == 3:
            days = ['Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy', 'Chủ Nhật']
            q = "Một tuần lễ có bao nhiêu ngày?"
            if is_duplicate(q):
                continue
            choices = ['5 ngày', '7 ngày', '30 ngày', '10 ngày']
            ans = 1
            steps = [{"text": "Một tuần lễ có 7 ngày: " + ', '.join(days) + ". ✅", "highlight": None}]
        elif pattern == 4:
            color = random.choice(['đỏ', 'xanh', 'vàng', 'tím'])
            other_color = random.choice([c for c in ['đỏ', 'xanh', 'vàng', 'tím'] if c != color])
            q = f"Trong hộp chỉ có toàn bóng màu {color}. Khẳng định nào dưới đây đúng?"
            if is_duplicate(q):
                continue
            correct = f"Chắc chắn lấy được bóng màu {color}."
            wrongs = [f"Có thể lấy được bóng màu {other_color}.", f"Không thể lấy được bóng màu {color}.", "Không lấy được quả bóng nào."]
            choices = [correct] + wrongs
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Vì hộp chỉ toàn bóng màu {color} nên chắc chắn lấy được bóng màu {color}. ✅", "highlight": None}]
        elif pattern == 5:
            color_a = random.choice(['đỏ', 'xanh'])
            color_b = 'vàng' if color_a != 'vàng' else 'tím'
            q = f"Hộp có cả bóng màu {color_a} và bóng màu {color_b}. Khẳng định nào dưới đây đúng khi lấy ngẫu nhiên 1 quả?"
            if is_duplicate(q):
                continue
            correct = f"Có thể lấy được bóng màu {color_a}."
            wrongs = [f"Chắc chắn lấy được bóng màu {color_a}.", f"Không thể lấy được bóng màu {color_b}.", "Chắc chắn không lấy được quả bóng nào."]
            choices = [correct] + wrongs
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Vì hộp có cả 2 màu nên có thể lấy được bóng màu {color_a} hoặc màu {color_b}. ✅", "highlight": None}]
        else:
            chosen_fruits = random.sample(FRUITS, 3)
            counts_list = random.sample(range(2, 10), 3)  # 3 số khác nhau, tránh hòa
            fruit_counts = dict(zip(chosen_fruits, counts_list))
            desc = '; '.join(f"{fr.split()[1]}: {c}" for fr, c in zip(chosen_fruits, counts_list))
            ask_type = random.choice(['most', 'least', 'total'])
            names_list = [fr.split()[1] for fr in chosen_fruits]
            q = f"Một biểu đồ tranh ghi lại số lượng trái cây: {desc}. "
            correct = None
            ans2 = None
            total = None
            if ask_type == 'most':
                q += "Loại nào có số lượng nhiều nhất?"
                correct = names_list[counts_list.index(max(counts_list))]
                choices = list(dict.fromkeys(names_list + ['dâu', 'na', 'mít']))[:4]
                if correct not in choices:
                    choices[0] = correct
            elif ask_type == 'least':
                q += "Loại nào có số lượng ít nhất?"
                correct = names_list[counts_list.index(min(counts_list))]
                choices = list(dict.fromkeys(names_list + ['dâu', 'na', 'mít']))[:4]
                if correct not in choices:
                    choices[0] = correct
            else:
                q += "Tổng cộng có bao nhiêu quả?"
                total = sum(counts_list)
                choices, ans2 = make_choices(total, incorrect_offset=4, min_val=3)
                correct = f"{total}"
            if is_duplicate(q):
                continue
            if ask_type in ('most', 'least'):
                random.shuffle(choices)
                ans = choices.index(correct)
                steps = [{"text": f"So sánh số lượng từng loại: {desc}. ✅", "highlight": None}]
            else:
                ans = ans2
                steps = [{"text": f"Cộng tất cả số lượng: {' + '.join(map(str, counts_list))} = {total}. ✅", "highlight": None}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK2 - 6. g2-muldiv25 : Bảng Nhân Chia 2 và 5
# ==================================================================
def gen_muldiv25(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])
        base = random.choice([2, 5])

        if pattern == 1:
            n = random.randint(1, 10)
            product = base * n
            q = f"{base} × {n} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(product, incorrect_offset=6, min_val=2)
            steps = [{"text": f"{base} × {n} = {product}. ✅", "highlight": "phep-nhan"}]
        elif pattern == 2:
            n = random.randint(1, 10)
            dividend = base * n
            q = f"{dividend} : {base} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(n, incorrect_offset=3, min_val=1)
            steps = [{"text": f"{dividend} : {base} = {n}. ✅", "highlight": "phep-chia"}]
        elif pattern == 3:
            n = random.randint(1, 10)
            product = base * n
            q = f"Trong phép tính {base} × {n} = {product}, số {product} được gọi là gì?"
            if is_duplicate(q):
                continue
            correct = "Tích"
            choices = ["Thừa số", "Tích", "Thương", "Số chia"]
            ans = choices.index(correct)
            steps = [{"text": f"Trong phép nhân, {base} và {n} là thừa số, {product} là tích. ✅", "highlight": "phep-nhan"}]
        elif pattern == 4:
            n = random.randint(1, 10)
            dividend = base * n
            q = f"Trong phép tính {dividend} : {base} = {n}, số {n} được gọi là gì?"
            if is_duplicate(q):
                continue
            correct = "Thương"
            choices = ["Số bị chia", "Số chia", "Thương", "Tích"]
            ans = choices.index(correct)
            steps = [{"text": f"Trong phép chia, {dividend} là số bị chia, {base} là số chia, {n} là thương. ✅", "highlight": "phep-chia"}]
        else:
            n = random.randint(1, 10)
            product = base * n
            q = f"Từ phép nhân {base} × {n} = {product}, viết được phép chia nào dưới đây?"
            if is_duplicate(q):
                continue
            correct = f"{product} : {base} = {n}"
            wrongs = [f"{product} : {n} = {base + 1}", f"{product} : {base + 1} = {n}", f"{product + n} : {base} = {n}"]
            choices = list(dict.fromkeys([correct] + wrongs))
            while len(choices) < 4:
                choices.append(f"{product} : {base} = {n + random.choice([1,2])}")
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Từ {base} × {n} = {product}, suy ra {product} : {base} = {n} (và {product} : {n} = {base}). ✅", "highlight": "phep-chia"}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK2 - 7. g2-numbers1000 : Các Số Đến 1000
# ==================================================================
def gen_numbers1000(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4])
        if pattern == 1:
            h = random.randint(1, 9)
            t = random.randint(0, 9)
            u = random.randint(0, 9)
            n = h * 100 + t * 10 + u
            q = f"Số gồm {h} trăm, {t} chục và {u} đơn vị được viết là:"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(n, incorrect_offset=50, min_val=100)
            steps = [{"text": f"{h} trăm + {t} chục + {u} đơn vị = {n}. ✅", "highlight": None}]
        elif pattern == 2:
            n = random.randint(101, 999)
            h, rem = divmod(n, 100)
            t, u = divmod(rem, 10)
            q = f"Phân tích số {n} thành tổng các trăm, chục, đơn vị:"
            if is_duplicate(q):
                continue
            correct = f"{h * 100} + {t * 10} + {u}"
            wrongs = set()
            while len(wrongs) < 3:
                wh, wt, wu = random.randint(1, 9), random.randint(0, 9), random.randint(0, 9)
                w = f"{wh * 100} + {wt * 10} + {wu}"
                if w != correct:
                    wrongs.add(w)
            choices = [correct] + list(wrongs)
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"{n} = {h * 100} + {t * 10} + {u}. ✅", "highlight": None}]
        elif pattern == 3:
            a = random.randint(100, 999)
            b = random.randint(100, 999)
            if a == b:
                continue
            q = f"So sánh: {a} ... {b}"
            if is_duplicate(q):
                continue
            correct = '<' if a < b else '>'
            choices = ['>', '<', '=', '?']
            ans = choices.index(correct)
            steps = [{"text": f"So sánh hàng trăm trước, rồi đến hàng chục, hàng đơn vị. Vậy {a} {correct} {b}. ✅", "highlight": None}]
        else:
            n = random.randint(101, 998)
            asks_next = random.random() < 0.5
            if asks_next:
                q = f"Số liền sau của số {n} là:"
                ans_val = n + 1
            else:
                q = f"Số liền trước của số {n} là:"
                ans_val = n - 1
            if is_duplicate(q):
                continue
            choices, ans = make_choices(ans_val, incorrect_offset=3, min_val=1)
            steps = [{"text": f"Kết quả là {ans_val}. ✅", "highlight": None}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK2 - 8. g2-addsub1000 : Cộng Trừ Trong Phạm Vi 1000
# ==================================================================
def gen_addsub1000(pid, topic_id):
    while True:
        is_add = random.random() < 0.5
        if is_add:
            a = random.randint(150, 799)
            b = random.randint(100, 799)
            total = a + b
            if total > 999:
                continue
            q = random.choice([f"Tính: {a} + {b} = ?", f"Đặt tính rồi tính: {a} + {b}"])
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=15, min_val=100)
            steps = [
                {"text": f"Cộng lần lượt từ hàng đơn vị: {a % 10} + {b % 10} = {a % 10 + b % 10}, viết và nhớ.", "highlight": "co-nho"},
                {"text": "Thực hiện tương tự với hàng chục và hàng trăm.", "highlight": "co-nho"},
                {"text": f"Kết quả: {total} ✅", "highlight": None},
            ]
        else:
            a = random.randint(300, 950)
            b = random.randint(100, a - 20)
            diff = a - b
            q = random.choice([f"Tính: {a} - {b} = ?", f"Đặt tính rồi tính: {a} - {b}"])
            if is_duplicate(q):
                continue
            choices, ans = make_choices(diff, incorrect_offset=15, min_val=1)
            steps = [
                {"text": "Trừ lần lượt từ hàng đơn vị, mượn khi cần.", "highlight": "phep-tru"},
                {"text": f"Kết quả: {diff} ✅", "highlight": None},
            ]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK2 - 9. g2-measureadv : Đo Lường Nâng Cao (m, km, kg, Tiền, Hình Khối)
# ==================================================================
def gen_measureadv(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])

        if pattern == 1:
            m = random.randint(1, 9)
            cm = m * 100
            to_cm = random.random() < 0.5
            q = f"Đổi đơn vị: {m} m = ... cm" if to_cm else f"Đổi đơn vị: {cm} cm = ... m"
            if is_duplicate(q):
                continue
            ans_val = cm if to_cm else m
            choices, ans = make_choices(ans_val, incorrect_offset=(30 if to_cm else 3), min_val=1)
            steps = [{"text": "Ta biết 1 m = 100 cm.", "highlight": None}, {"text": f"Kết quả là {ans_val}. ✅", "highlight": None}]
        elif pattern == 2:
            km = random.randint(1, 9)
            m = km * 1000
            to_m = random.random() < 0.5
            q = f"Đổi đơn vị: {km} km = ... m" if to_m else f"Đổi đơn vị: {m} m = ... km"
            if is_duplicate(q):
                continue
            ans_val = m if to_m else km
            choices, ans = make_choices(ans_val, incorrect_offset=(300 if to_m else 3), min_val=1)
            steps = [{"text": "Ta biết 1 km = 1000 m.", "highlight": None}, {"text": f"Kết quả là {ans_val}. ✅", "highlight": None}]
        elif pattern == 3:
            animal_a, animal_b, w_min, w_max = random.choice(ANIMAL_PAIRS)
            wa = random.randint(w_min, w_max)
            max_diff = min(wa - 1, max(w_max // 4, 3))
            diff = random.randint(1, max(max_diff, 1))
            wb = wa - diff
            if wb < 1:
                continue
            q = f"Con {animal_a} cân nặng {wa}kg, con {animal_b} nhẹ hơn {animal_a} {diff}kg. Hỏi con {animal_b} cân nặng bao nhiêu?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(wb, unit='kg', incorrect_offset=8, min_val=1)
            steps = [
                {"text": "Bài toán \"nhẹ hơn\" -> dùng phép trừ.", "highlight": "phep-tru"},
                {"text": f"{wa} - {diff} = {wb} (kg). ✅", "highlight": None},
            ]
        elif pattern == 4:
            denominations = [100, 200, 500, 1000]
            a, b = random.sample(denominations, 2)
            q = f"So sánh giá trị: tờ {a} đồng và tờ {b} đồng, tờ nào có mệnh giá lớn hơn?"
            if is_duplicate(q):
                continue
            correct = f"Tờ {max(a, b)} đồng"
            wrong_denom = random.choice([d for d in denominations if d not in (a, b)])
            choices = [f"Tờ {a} đồng", f"Tờ {b} đồng", "Bằng nhau", f"Tờ {wrong_denom} đồng"]
            choices = list(dict.fromkeys(choices))
            if correct not in choices:
                choices.append(correct)
            while len(choices) < 4:
                choices.append("Không xác định được")
            ans = choices.index(correct)
            steps = [{"text": f"{max(a,b)} > {min(a,b)} nên tờ {max(a,b)} đồng có giá trị lớn hơn. ✅", "highlight": None}]
        else:
            obj, shape = random.choice(SOLID_EXAMPLES)
            q = f"{obj.capitalize()} thường có dạng hình khối nào?"
            if is_duplicate(q):
                continue
            all_shapes = ['khối trụ', 'khối cầu', 'hình tứ giác', 'khối lập phương']
            correct = shape
            choices = all_shapes[:]
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"{obj.capitalize()} có dạng {shape}. ✅", "highlight": None}]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# HK2 - 10. g2-wordmuldiv : Giải Toán Nhân Chia
# ==================================================================
def gen_wordmuldiv(pid, topic_id):
    while True:
        pattern = random.choice([1, 2])
        if pattern == 1:
            fruit = random.choice(FRUITS)
            box = random.choice(BOXES)
            a = random.randint(2, 9)
            b = random.randint(2, 9)
            product = a * b
            fruit_noun = fruit.split()[1]
            q = f"Mỗi {box} có {a} {fruit}. Có {b} {box}. Hỏi tất cả có bao nhiêu {fruit_noun}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(product, incorrect_offset=6, min_val=4)
            steps = [
                {"text": f"Có {b} {box}, mỗi {box} {a} quả -> dùng phép nhân.", "highlight": "phep-nhan"},
                {"text": f"{a} × {b} = {product} ✅", "highlight": None},
            ]
        else:
            item = random.choice(SCHOOL_ITEMS)
            groups = random.randint(2, 9)
            per = random.randint(2, 9)
            total = groups * per
            q = f"Có {total} {item} chia đều cho {groups} bạn. Hỏi mỗi bạn được bao nhiêu {item}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(per, unit=f' {item}', incorrect_offset=3, min_val=1)
            steps = [
                {"text": "Chia đều là thực hiện phép tính chia.", "highlight": "phep-chia"},
                {"text": f"{total} : {groups} = {per} ({item}) ✅", "highlight": None},
            ]
        return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# 11 & 12. Đề Giữa Kỳ (ôn HK1) / Đề Cuối Kỳ (ôn HK2)
# ==================================================================
HK1_GENERATORS = [gen_numbers100, gen_addsub100, gen_geomeasure, gen_wordproblem, gen_clockstats]
HK2_GENERATORS = [gen_muldiv25, gen_numbers1000, gen_addsub1000, gen_measureadv, gen_wordmuldiv]

def gen_exam(pid, topic_id, generators, label):
    fn = random.choice(generators)
    base = fn(pid, topic_id)
    prefixed_q = f"{label}: {base['question']}"
    if is_duplicate(prefixed_q):
        return None
    base['question'] = prefixed_q
    base['topicId'] = topic_id
    return base


def gen_midterm(pid, topic_id):
    while True:
        result = gen_exam(pid, topic_id, HK1_GENERATORS, "Đề Giữa Kỳ")
        if result is not None:
            return result


def gen_final(pid, topic_id):
    while True:
        result = gen_exam(pid, topic_id, HK2_GENERATORS, "Đề Cuối Kỳ")
        if result is not None:
            return result


# ==================================================================
# ĐỊNH NGHĨA 12 CHỦ ĐỀ MỚI + CẤU HÌNH DI TRÚ TỪ CHỦ ĐỀ CŨ
# ==================================================================
NEW_TOPICS = [
    {"id": "g2-numbers100", "name": "Số Đến 100", "generator": gen_numbers100},
    {"id": "g2-addsub100", "name": "Cộng Trừ Có Nhớ (Phạm Vi 100)", "generator": gen_addsub100},
    {"id": "g2-geomeasure", "name": "Hình Học & Đo Lường (cm, dm, lít)", "generator": gen_geomeasure},
    {"id": "g2-wordproblem", "name": "Giải Toán Có Lời Văn (Nhiều Hơn - Ít Hơn)", "generator": gen_wordproblem},
    {"id": "g2-clockstats", "name": "Xem Giờ & Thống Kê Xác Suất", "generator": gen_clockstats},
    {"id": "g2-muldiv25", "name": "Bảng Nhân Chia 2 và 5", "generator": gen_muldiv25},
    {"id": "g2-numbers1000", "name": "Các Số Đến 1000", "generator": gen_numbers1000},
    {"id": "g2-addsub1000", "name": "Cộng Trừ Trong Phạm Vi 1000", "generator": gen_addsub1000},
    {"id": "g2-measureadv", "name": "Đo Lường Nâng Cao (m, km, kg, Tiền, Hình Khối)", "generator": gen_measureadv},
    {"id": "g2-wordmuldiv", "name": "Giải Toán Nhân Chia", "generator": gen_wordmuldiv},
    {"id": "g2-midterm", "name": "Đề Giữa Kỳ (Ôn Tập Học Kỳ 1)", "generator": gen_midterm},
    {"id": "g2-final", "name": "Đề Cuối Kỳ (Ôn Tập Học Kỳ 2)", "generator": gen_final},
]

def old_add_filter(p):
    nums = re.findall(r'\d+', p['question'])
    return len(nums) >= 1 and max(len(n) for n in nums) <= 2

def old_add_filter_1000(p):
    nums = re.findall(r'\d+', p['question'])
    return len(nums) >= 1 and max(len(n) for n in nums) == 3

def old_mul_filter_25(p):
    nums = [int(n) for n in re.findall(r'\d+', p['question'])]
    return len(nums) >= 2 and (2 in nums[:2] or 5 in nums[:2])

def old_measure_kg_filter(p):
    return 'kg' in p['question']

def old_measure_lit_filter(p):
    return 'lít' in p['question']

MIGRATIONS = [
    ("g2-clock", lambda p: True, "g2-clockstats", 55),
    ("g2-add", old_add_filter, "g2-addsub100", 55),
    ("g2-sub", lambda p: True, "g2-addsub100", 55),
    ("g2-add", old_add_filter_1000, "g2-addsub1000", 30),
    ("g2-mul", old_mul_filter_25, "g2-muldiv25", 40),
    ("g2-measure", old_measure_kg_filter, "g2-measureadv", 40),
    ("g2-measure", old_measure_lit_filter, "g2-geomeasure", 20),
]

OLD_TOPIC_IDS = ["g2-clock", "g2-add", "g2-sub", "g2-mul", "g2-findx", "g2-measure", "g2-midterm", "g2-final"]


def main():
    print("Đọc topics.js và problems.js...")
    with open('src/data/topics.js', 'r', encoding='utf-8') as f:
        topics = json.loads(re.search(r'export const topics = (\{[\s\S]*?\});', f.read()).group(1))
    with open('src/data/problems.js', 'r', encoding='utf-8') as f:
        problems = json.loads(re.search(r'export const problems = (\{[\s\S]*?\});', f.read()).group(1))

    for pid, prob in problems.items():
        if 'question' in prob:
            generated_questions.add(re.sub(r'\s+', ' ', prob['question']).strip().lower())

    old_problems_by_topic = {}
    for pid, p in problems.items():
        if p.get('topicId') in OLD_TOPIC_IDS:
            old_problems_by_topic.setdefault(p['topicId'], []).append(p)

    removed = 0
    for pid in list(problems.keys()):
        if problems[pid].get('topicId') in OLD_TOPIC_IDS:
            q_norm = re.sub(r'\s+', ' ', problems[pid]['question']).strip().lower()
            generated_questions.discard(q_norm)
            del problems[pid]
            removed += 1
    print(f"Đã gỡ {removed} bài thuộc 8 chủ đề cũ khỏi problems.js (sẽ di trú lại phần phù hợp).")

    new_topic_list = []
    new_topics_map = {}
    for t in NEW_TOPICS:
        entry = {"id": t["id"], "name": t["name"], "problemIds": []}
        new_topic_list.append(entry)
        new_topics_map[t["id"]] = entry
    topics['2'] = new_topic_list

    migrate_idx = 1
    for old_id, filter_fn, new_id, max_take in MIGRATIONS:
        pool = old_problems_by_topic.get(old_id, [])
        taken = 0
        for p in pool:
            if taken >= max_take:
                break
            if not filter_fn(p):
                continue
            q_norm = re.sub(r'\s+', ' ', p['question']).strip().lower()
            if q_norm in generated_questions:
                continue
            new_pid = f"{new_id}-migrated-{migrate_idx}"
            migrate_idx += 1
            new_p = dict(p)
            new_p['id'] = new_pid
            new_p['topicId'] = new_id
            problems[new_pid] = new_p
            new_topics_map[new_id]['problemIds'].append(new_pid)
            generated_questions.add(q_norm)
            taken += 1
        print(f"Di trú {old_id} -> {new_id}: giữ lại {taken} bài (đã lọc theo nội dung).")

    for t in NEW_TOPICS:
        entry = new_topics_map[t['id']]
        current = len(entry['problemIds'])
        need = TARGET - current
        print(f"Chủ đề '{t['id']}' ({t['name']}): đang có {current} bài (di trú), cần sinh thêm {max(need,0)}.")
        if need <= 0:
            entry['problemIds'] = entry['problemIds'][:TARGET]
            continue
        idx = 1
        gen_count = 0
        attempts = 0
        max_attempts = TARGET * 60
        while len(entry['problemIds']) < TARGET and attempts < max_attempts:
            attempts += 1
            new_pid = f"{t['id']}-gen3-{idx}"
            while new_pid in problems:
                idx += 1
                new_pid = f"{t['id']}-gen3-{idx}"
            prob = t['generator'](new_pid, t['id'])
            problems[new_pid] = prob
            entry['problemIds'].append(new_pid)
            gen_count += 1
            idx += 1
        print(f"-> Đã sinh thêm {gen_count} bài. Tổng: {len(entry['problemIds'])}")

    with open('src/data/topics.js', 'w', encoding='utf-8') as f:
        f.write(f"export const topics = {json.dumps(topics, ensure_ascii=False, indent=2)};\n")

    referenced = set()
    for t in topics['2']:
        referenced.update(t['problemIds'])
    orphans = [pid for pid in problems if pid.startswith('g2-') and pid not in referenced]
    for pid in orphans:
        del problems[pid]
    print(f"Đã dọn {len(orphans)} bài 'mồ côi' (bị cắt bớt do vượt TARGET nhưng còn sót trong problems.js).")

    with open('src/data/problems.js', 'w', encoding='utf-8') as f:
        f.write(f"export const problems = {json.dumps(problems, ensure_ascii=False, indent=2)};\n")
    print("\nĐã ghi đè topics.js và problems.js. Hoàn thành tái cấu trúc Lớp 2.")


if __name__ == '__main__':
    main()
