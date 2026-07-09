import json
import re
import random

# Seed cố định để kết quả có thể tái lập
random.seed(2607)

NAMES = ['Lan', 'Bình', 'Hoa', 'Huy', 'Minh', 'Tuấn', 'Mai', 'An', 'Nam', 'Trang', 'Linh', 'Phong', 'Hương', 'Đức', 'Vy', 'Hùng']
FRUITS = ['quả táo 🍎', 'quả cam 🍊', 'quả chuối 🍌', 'quả dâu 🍓', 'quả bưởi 🍈', 'quả lê 🍐', 'quả đào 🍑', 'quả quýt 🍊']
BOXES = ['hộp', 'rổ', 'giỏ', 'túi', 'thùng']
# (con A, con B, cân nặng tối thiểu, cân nặng tối đa) - khoảng cân nặng thực tế theo từng loại vật
ANIMAL_PAIRS = [
    ('lợn', 'chó', 15, 60),
    ('trâu', 'bò', 150, 400),
    ('ngựa', 'dê', 80, 250),
    ('gà', 'vịt', 1, 4),
]
LIQUIDS = ['nước mắm', 'nước cam', 'sữa', 'dầu ăn', 'nước']
GOODS = ['gạo', 'đường', 'bột mì', 'muối', 'ngô']

# ===== Chống trùng lặp =====
generated_questions = set()

def is_duplicate(question_text):
    normalized = re.sub(r'\s+', ' ', question_text).strip().lower()
    if normalized in generated_questions:
        return True
    generated_questions.add(normalized)
    return False


def make_choices(correct_val, unit='', incorrect_offset=10, min_val=0):
    """Sinh 4 phương án (gồm đáp án đúng), giá trị là số nguyên."""
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


# ==================================================================
# g2-clock : Xem Giờ
# ==================================================================
def generate_clock_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4])
        hour = random.randint(1, 11)
        next_hour = hour + 1 if hour < 12 else 1

        if pattern == 1:
            n = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            minute = n * 5
            q = f"Kim ngắn chỉ giữa số {hour} và {next_hour}, kim dài chỉ số {n}. Bây giờ là mấy giờ?"
            if is_duplicate(q):
                continue
            correct = f"{hour} giờ {minute} phút"
            wrongs = set()
            while len(wrongs) < 3:
                w_n = random.choice([x for x in range(1, 12) if x != n])
                w = f"{hour} giờ {w_n * 5} phút"
                if w != correct:
                    wrongs.add(w)
            choices = [correct] + list(wrongs)
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [
                {"text": f"Kim ngắn ở giữa {hour} và {next_hour} nghĩa là hơn {hour} giờ.", "highlight": "xem-gio"},
                {"text": f"Kim dài chỉ số {n} tương ứng với {n} × 5 = {minute} phút.", "highlight": "kim-dong-ho"},
                {"text": f"Vậy là {correct}. ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 2:
            n = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])
            minute = n * 5
            q = f"Đồng hồ chỉ {hour} giờ {minute} phút. Kim dài đang chỉ vào số mấy?"
            if is_duplicate(q):
                continue
            wrongs = set()
            while len(wrongs) < 3:
                w_n = random.randint(1, 11)
                if w_n != n:
                    wrongs.add(w_n)
            choices = [f"Số {n}"] + [f"Số {w}" for w in wrongs]
            random.shuffle(choices)
            ans = choices.index(f"Số {n}")
            steps = [
                {"text": "Mỗi số trên đồng hồ cách nhau 5 phút.", "highlight": "kim-dong-ho"},
                {"text": f"{minute} phút tương ứng với {minute} ÷ 5 = {n}.", "highlight": None},
                {"text": f"Vậy kim dài chỉ vào số {n}. ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 3:
            name = random.choice(NAMES)
            start_h = random.randint(1, 9)
            start_m = random.choice([0, 15, 30])
            duration = random.choice([15, 30, 45])
            end_m = start_m + duration
            end_h = start_h
            if end_m >= 60:
                end_m -= 60
                end_h += 1
            activity = random.choice(['làm bài tập', 'đọc sách', 'chơi cờ vua', 'tập thể dục', 'vẽ tranh'])
            start_str = f"{start_h} giờ" if start_m == 0 else f"{start_h} giờ {start_m} phút"
            end_str = f"{end_h} giờ" if end_m == 0 else f"{end_h} giờ {end_m} phút"
            q = f"{name} bắt đầu {activity} lúc {start_str} và làm xong lúc {end_str}. {name} đã làm trong bao lâu?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(duration, unit=' phút', incorrect_offset=15, min_val=5)
            steps = [
                {"text": f"Từ {start_str} đến {end_str} là trôi qua {duration} phút. ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        else:
            q = f"Đồng hồ chỉ {hour} giờ rưỡi. '{hour} giờ rưỡi' còn được gọi là mấy giờ mấy phút?"
            if is_duplicate(q):
                continue
            correct = f"{hour} giờ 30 phút"
            wrongs = [f"{hour} giờ 15 phút", f"{hour} giờ 45 phút", f"{next_hour} giờ 30 phút"]
            choices = [correct] + wrongs
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [
                {"text": "'Giờ rưỡi' tương ứng với 30 phút.", "highlight": "xem-gio"},
                {"text": f"Vậy là {correct}. ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# g2-add : Cộng Có Nhớ
# ==================================================================
def generate_add_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3])
        if pattern in (1, 2):
            a = random.randint(15, 89)
            b = random.randint(15, 89)
            a_dv, b_dv = a % 10, b % 10
            if a_dv + b_dv < 10:
                b = b - b_dv + (10 - a_dv) if a_dv > 0 else b + 5
                b = min(b, 89)
            total = a + b
            prefix = "Tính: " if pattern == 2 else ""
            q = f"{prefix}{a} + {b} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=8, min_val=10)
            dv = a % 10 + b % 10
            steps = [
                {"text": f"Cộng hàng đơn vị: {a % 10} + {b % 10} = {dv}. Viết {dv % 10}, nhớ {dv // 10}.", "highlight": "co-nho"},
                {"text": f"Cộng hàng chục: {a // 10} + {b // 10} + {dv // 10}(nhớ) = {total // 10}.", "highlight": "co-nho"},
                {"text": f"Kết quả: {total} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        else:
            a = random.randint(200, 799)
            b = random.randint(100, 599)
            total = a + b
            q = f"Tính: {a} + {b} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=12, min_val=100)
            steps = [
                {"text": f"{a % 10} + {b % 10} = {a % 10 + b % 10}, viết và nhớ như cộng có nhớ.", "highlight": "co-nho"},
                {"text": "Thực hiện tương tự với hàng chục và hàng trăm.", "highlight": "co-nho"},
                {"text": f"Kết quả: {total} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# g2-sub : Trừ Có Nhớ
# ==================================================================
def generate_sub_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3])
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

        if pattern == 1:
            q = f"{a} - {b} = ?"
        elif pattern == 2:
            q = f"Tìm M: M = {a} - {b}"
        else:
            q = f"Đặt tính rồi tính: {a} - {b} = ?"
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
# g2-mul : Bảng Nhân
# ==================================================================
def generate_mul_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3])
        a = random.randint(2, 10)
        b = random.randint(2, 10)
        product = a * b

        if pattern == 1:
            q = f"{a} × {b} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(product, incorrect_offset=6, min_val=4)
            steps = [
                {"text": f"{a} × {b} có nghĩa là cộng số {a} {b} lần.", "highlight": "phep-nhan"},
                {"text": f"Kết quả: {a} × {b} = {product} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 2:
            q = f"Tính phép nhân: {a} × {b}"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(product, incorrect_offset=6, min_val=4)
            steps = [{"text": f"{a} nhân {b} bằng {product}.", "highlight": "phep-nhan"}]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        else:
            fruit = random.choice(FRUITS)
            box = random.choice(BOXES)
            fruit_noun = fruit.split()[1]
            q = f"Mỗi {box} có {a} {fruit}. Có {b} {box}. Hỏi tất cả có bao nhiêu {fruit_noun}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(product, incorrect_offset=6, min_val=4)
            steps = [
                {"text": f"Có {b} {box}, mỗi {box} {a} quả -> dùng phép nhân.", "highlight": "phep-nhan"},
                {"text": f"{a} × {b} = {product} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# g2-findx : Tìm X
# ==================================================================
def generate_findx_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4])
        a = random.randint(10, 60)
        x = random.randint(5, 60)

        if pattern == 1:
            b = a + x
            q = f"Tìm x: x + {a} = {b}"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(x, incorrect_offset=8, min_val=1)
            steps = [
                {"text": "x là số hạng chưa biết. Muốn tìm số hạng chưa biết, ta lấy tổng trừ đi số hạng đã biết.", "highlight": "phep-tru"},
                {"text": f"x = {b} - {a} = {x} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 2:
            b = x - a if x > a else x + a
            b = max(b, 1)
            result = b + a
            q = f"Tìm x: x - {a} = {b}"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(result, incorrect_offset=8, min_val=1)
            steps = [
                {"text": "x là số bị trừ. Muốn tìm số bị trừ, ta lấy hiệu cộng với số trừ.", "highlight": "phep-cong"},
                {"text": f"x = {b} + {a} = {result} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 3:
            total = a + random.randint(10, 50)
            result = total - a
            q = f"Tìm x: {total} - x = {a}"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(result, incorrect_offset=8, min_val=1)
            steps = [
                {"text": "x là số trừ. Muốn tìm số trừ, ta lấy số bị trừ trừ đi hiệu.", "highlight": "phep-tru"},
                {"text": f"x = {total} - {a} = {result} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        else:
            aa = random.randint(20, 90)
            bb = random.randint(10, aa - 5)
            result = aa - bb
            q = f"Tìm M: M = {aa} - {bb}"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(result, incorrect_offset=8, min_val=0)
            steps = [{"text": f"Trừ có mượn: {aa} - {bb} = {result}.", "highlight": "phep-tru"}]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# g2-measure : Đo Lường (kg, l)
# ==================================================================
def generate_measure_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])
        animal_a, animal_b, w_min, w_max = random.choice(ANIMAL_PAIRS)

        if pattern == 1:
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
                {"text": f"{wa} - {diff} = {wb} (kg). Con {animal_b} nặng {wb}kg ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 2:
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
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 3:
            wa = random.randint(w_min, w_max // 2 if w_max > 10 else w_max)
            extra = random.randint(1, max(w_max // 4, 2))
            wb = wa + extra
            total = wa + wb
            q = f"{animal_a.capitalize()} cân nặng {wa}kg. {animal_b.capitalize()} nặng thêm {extra}kg. Cả hai nặng bao nhiêu?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, unit='kg', incorrect_offset=10, min_val=5)
            steps = [{"text": f"{animal_b.capitalize()}: {wa} + {extra} = {wb}kg. Tổng = {wa} + {wb} = {total}kg.", "highlight": "phep-cong"}]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        elif pattern == 4:
            good = random.choice(GOODS)
            total = random.randint(20, 90)
            taken = random.randint(5, total - 5)
            remain = total - taken
            q = f"Kho có {total}kg {good}. Người ta lấy ra {taken}kg. Trong kho còn lại bao nhiêu kg {good}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(remain, unit='kg', incorrect_offset=8, min_val=1)
            steps = [
                {"text": "Lấy ra làm giảm số lượng -> dùng phép trừ.", "highlight": "phep-tru"},
                {"text": f"{total} - {taken} = {remain} (kg) ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        else:
            good = random.choice(GOODS)
            per_bag = random.randint(2, 9)
            bags = random.randint(2, 9)
            total = per_bag * bags
            q = f"Mỗi túi {good} nặng {per_bag}kg. Có {bags} túi. Tất cả nặng bao nhiêu kg?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, unit='kg', incorrect_offset=8, min_val=4)
            steps = [
                {"text": "Nhiều túi cùng khối lượng -> dùng phép nhân.", "highlight": "phep-nhan"},
                {"text": f"{per_bag} × {bags} = {total} (kg) ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


# ==================================================================
# g2-midterm / g2-final : Đề kiểm tra (tổng hợp)
# ==================================================================
def generate_exam_problem(pid, topic_id, is_final):
    label = "Đề thi Cuối Kỳ" if is_final else "Đề Kiểm Tra Giữa Kỳ"
    while True:
        pattern = random.randint(1, 6)

        if pattern == 1:
            start = random.randint(100, 950) if is_final else random.randint(100, 990)
            end = start + 10
            q = f"{label}: Dãy số nào gồm các số từ {start} đến {end}?"
            if is_duplicate(q):
                continue
            correct = ', '.join(str(n) for n in range(start, end + 1))
            wrong1 = ', '.join(str(n) for n in range(start, end + 1, 2))
            wrong2 = f"{start - 1}, {start}, {start + 1}, {start + 2}"
            wrong3 = ', '.join(str(n) for n in range(start, end + 10, 10))
            choices = [correct, wrong1, wrong2, wrong3]
            random.shuffle(choices)
            ans = choices.index(correct)
            steps = [{"text": f"Đếm lần lượt từng đơn vị từ {start} đến {end}.", "highlight": None}]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 2:
            a = random.randint(150, 799)
            b = random.randint(120, 799)
            total = a + b
            q = f"{label}: Tính: {a} + {b} = ?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(total, incorrect_offset=12, min_val=100)
            steps = [
                {"text": f"{a % 10} + {b % 10} = {a % 10 + b % 10}, viết và nhớ như cộng có nhớ.", "highlight": "co-nho"},
                {"text": f"Kết quả: {total} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 3:
            groups = random.randint(2, 9)
            per = random.randint(2, 9)
            total = groups * per
            noun = random.choice(['học sinh', 'quyển vở', 'cây bút', 'chiếc kẹo'])
            q = f"{label}: Một lớp có {total} {noun}, chia đều thành {groups} tổ. Hỏi mỗi tổ có bao nhiêu {noun}?"
            if is_duplicate(q):
                continue
            choices, ans = make_choices(per, unit=f' {noun}', incorrect_offset=3, min_val=1)
            steps = [
                {"text": "Chia đều là thực hiện phép tính chia.", "highlight": "phep-chia"},
                {"text": f"Phép tính: {total} ÷ {groups} = {per}.", "highlight": None},
                {"text": f"Đáp số: {per} {noun} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 4:
            a = random.randint(100, 999)
            offset = random.randint(1, 30)
            b = a + offset if random.random() < 0.5 else a - offset
            if b == a or b < 0:
                continue
            q = f"{label}: So sánh: {a} ... {b}"
            if is_duplicate(q):
                continue
            correct = '<' if a < b else '>'
            choices = ['>', '<', '=', '?']
            ans = choices.index(correct)
            steps = [
                {"text": f"So sánh từng hàng của {a} và {b} từ trái sang phải.", "highlight": None},
                {"text": f"Vậy {a} {correct} {b} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        elif pattern == 5:
            kg = random.randint(1, 9)
            grams = kg * 1000
            q = f"{label}: Đổi đơn vị: {grams}g = ... kg"
            if is_duplicate(q):
                continue
            choices = [f"{kg} kg", f"{kg * 10} kg", f"{kg * 100} kg", f"0.{kg} kg"]
            random.shuffle(choices)
            ans = choices.index(f"{kg} kg")
            steps = [
                {"text": "Ta biết 1000g = 1kg.", "highlight": None},
                {"text": f"Vậy {grams}g = {grams} ÷ 1000 = {kg}kg ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

        else:
            price = random.randint(5, 30) * 1000
            qty = random.randint(2, 9)
            total = price * qty
            good = random.choice(['cam', 'táo', 'xoài', 'ổi', 'nho'])

            def fmt_money(n):
                return f"{n:,}".replace(",", ".") + " đồng"

            price_str = fmt_money(price)
            total_str = fmt_money(total)
            q = f"{label}: Mẹ mua {qty} kg {good}, mỗi kg giá {price_str}. Hỏi mẹ phải trả bao nhiêu tiền?"
            if is_duplicate(q):
                continue

            wrong_vals = set()
            while len(wrong_vals) < 3:
                offset = random.randint(-3, 3)
                if offset == 0:
                    continue
                w = total + offset * price
                if w > 0 and w != total:
                    wrong_vals.add(w)
            choices = [fmt_money(total)] + [fmt_money(w) for w in wrong_vals]
            random.shuffle(choices)
            ans = choices.index(fmt_money(total))
            steps = [
                {"text": "Mua nhiều món cùng giá ta dùng phép nhân.", "highlight": "phep-nhan"},
                {"text": f"Phép tính: {price_str} × {qty} = {total_str}.", "highlight": None},
                {"text": f"Đáp số: {total_str} ✅", "highlight": None},
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}


GENERATORS = {
    'g2-clock': generate_clock_problem,
    'g2-add': generate_add_problem,
    'g2-sub': generate_sub_problem,
    'g2-mul': generate_mul_problem,
    'g2-findx': generate_findx_problem,
    'g2-measure': generate_measure_problem,
    'g2-midterm': lambda pid, tid: generate_exam_problem(pid, tid, is_final=False),
    'g2-final': lambda pid, tid: generate_exam_problem(pid, tid, is_final=True),
}


def main():
    target = 100
    print("Bắt đầu đọc topics.js và problems.js...")

    with open('src/data/topics.js', 'r', encoding='utf-8') as f:
        topics_content = f.read()
    topics_match = re.search(r'export const topics = (\{[\s\S]*?\});', topics_content)
    topics = json.loads(topics_match.group(1))

    with open('src/data/problems.js', 'r', encoding='utf-8') as f:
        problems_content = f.read()
    problems_match = re.search(r'export const problems = (\{[\s\S]*?\});', problems_content)
    problems = json.loads(problems_match.group(1))

    for pid, prob in problems.items():
        if 'question' in prob:
            normalized = re.sub(r'\s+', ' ', prob['question']).strip().lower()
            generated_questions.add(normalized)

    grade2_topics = topics.get("2", [])
    print(f"Số lượng chủ đề Lớp 2 tìm thấy: {len(grade2_topics)}")

    for topic in grade2_topics:
        t_id = topic['id']
        t_name = topic['name']
        prob_ids = topic.setdefault('problemIds', [])
        gen_fn = GENERATORS.get(t_id)

        current_count = len(prob_ids)
        need = target - current_count
        print(f"Chủ đề '{t_id}' ({t_name}): Đang có {current_count} bài. Cần sinh thêm {max(need,0)} bài.")

        if need <= 0 or gen_fn is None:
            if gen_fn is None:
                print(f"-> CẢNH BÁO: chưa có generator cho '{t_id}', bỏ qua.")
            continue

        idx = current_count + 1
        generated_count = 0
        max_attempts = target * 50
        attempts = 0

        while len(prob_ids) < target and attempts < max_attempts:
            attempts += 1
            new_pid = f"{t_id}-gen2-{idx}"
            while new_pid in problems:
                idx += 1
                new_pid = f"{t_id}-gen2-{idx}"

            prob = gen_fn(new_pid, t_id)
            problems[new_pid] = prob
            prob_ids.append(new_pid)
            generated_count += 1
            idx += 1

        print(f"-> Đã sinh {generated_count} bài cho '{t_id}'. Tổng số bây giờ: {len(prob_ids)}")

    with open('src/data/topics.js', 'w', encoding='utf-8') as f:
        f.write(f"export const topics = {json.dumps(topics, ensure_ascii=False, indent=2)};\n")
    print("Đã ghi đè lại src/data/topics.js!")

    with open('src/data/problems.js', 'w', encoding='utf-8') as f:
        f.write(f"export const problems = {json.dumps(problems, ensure_ascii=False, indent=2)};\n")
    print("Đã ghi đè lại src/data/problems.js!")

    print("\nHoàn thành sinh bài tập tự động cho Lớp 2.")


if __name__ == '__main__':
    main()
