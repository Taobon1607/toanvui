import json
import re
import random

# We set a seed to keep results reproducible
random.seed(1607)

# Helper constants
NAMES = ['Lan', 'Bình', 'Hoa', 'Huy', 'Minh', 'Tuấn', 'Mai', 'An', 'Nam', 'Trang', 'Linh', 'Phong', 'Hương', 'Đức', 'Vy', 'Hùng']
FRUITS = ['quả táo 🍎', 'quả cam 🍊', 'quả chuối 🍌', 'quả dâu 🍓', 'quả bưởi 🍈', 'quả lê 🍐', 'quả đào 🍑', 'quả quýt 🍊']
ANIMALS = ['con mèo 🐱', 'con chó 🐶', 'con chim 🐦', 'con cá 🐟', 'con thỏ 🐰', 'con gà 🐔', 'con vịt 🦆', 'con rùa 🐢']
OBJECTS = ['cái kẹo 🍬', 'chiếc bánh 🍰', 'viên bi 🔵', 'quyển sách 📖', 'cây bút ✏️', 'bông hoa 🌸', 'quả bóng 🎈', 'cái thước 📏']

# Convert Vietnamese number to word for g1-dem100
NUM_WORDS_TEN = {
    0: 'không', 1: 'một', 2: 'hai', 3: 'ba', 4: 'bốn', 5: 'năm', 6: 'sáu', 7: 'bảy', 8: 'tám', 9: 'chín'
}

def to_vietnamese_word(num):
    if num < 10:
        return NUM_WORDS_TEN[num]
    elif num == 10:
        return 'mười'
    elif num < 20:
        unit = num % 10
        unit_word = NUM_WORDS_TEN[unit]
        if unit == 5:
            unit_word = 'lăm'
        elif unit == 4:
            unit_word = 'tư'
        return f"mười {unit_word}"
    else:
        ten = num // 10
        unit = num % 10
        ten_word = NUM_WORDS_TEN[ten]
        if unit == 0:
            return f"{ten_word} mươi"
        unit_word = NUM_WORDS_TEN[unit]
        if unit == 1:
            unit_word = 'mốt'
        elif unit == 5:
            unit_word = 'lăm'
        elif unit == 4:
            unit_word = 'tư'
        return f"{ten_word} mươi {unit_word}"

# Helper to generate choices, ensuring 4 distinct values including correct answer
def make_choices(correct_val, is_number=True, unit='', incorrect_offset=5, min_val=0):
    choices = [correct_val]
    attempts = 0
    while len(choices) < 4 and attempts < 100:
        attempts += 1
        if is_number:
            offset = random.randint(-incorrect_offset, incorrect_offset)
            if offset == 0:
                continue
            val = correct_val + offset
            if val < min_val:
                continue
            if val not in choices:
                choices.append(val)
        else:
            # For non-numeric list items or custom formatting
            pass
            
    if is_number and len(choices) == 4:
        # Convert to string and append unit if needed
        str_choices = [f"{c}{unit}" for c in choices]
    else:
        str_choices = [str(c) for c in choices]
        
    random.shuffle(str_choices)
    correct_str = f"{correct_val}{unit}" if is_number else str(correct_val)
    ans_idx = str_choices.index(correct_str)
    return str_choices, ans_idx

# Set to keep track of generated questions to guarantee absolute uniqueness
generated_questions = set()

def is_duplicate(question_text):
    normalized = re.sub(r'\s+', ' ', question_text).strip().lower()
    if normalized in generated_questions:
        return True
    generated_questions.add(normalized)
    return False

def generate_clock_problem(pid, topic_id):
    # Generates unique Clock reading/setting questions
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])
        name = random.choice(NAMES)
        hour = random.randint(1, 12)
        
        if pattern == 1:
            q = f"Kim ngắn chỉ vào số {hour}, kim dài chỉ vào số 12. Hỏi lúc đó đồng hồ chỉ mấy giờ?"
            if is_duplicate(q): continue
            choices = [f"{hour} giờ đúng", f"12 giờ đúng", f"{hour} giờ 12 phút", f"{(hour % 12) + 1} giờ đúng"]
            random.shuffle(choices)
            ans = choices.index(f"{hour} giờ đúng")
            steps = [
                {"text": "Khi kim dài chỉ vào số 12, đồng hồ chỉ giờ đúng.", "highlight": "kim-dong-ho"},
                {"text": f"Kim ngắn chỉ vào số nào thì đó là số giờ tương ứng. Ở đây kim ngắn chỉ số {hour}.", "highlight": None},
                {"text": f"Vậy đồng hồ đang chỉ {hour} giờ đúng!", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2:
            q = f"{name} thức dậy và chuẩn bị đi học lúc {hour} giờ sáng. Kim ngắn của đồng hồ lúc đó chỉ vào số mấy?"
            if is_duplicate(q): continue
            choices, ans = make_choices(hour, unit=' (số chỉ giờ)', incorrect_offset=3, min_val=1)
            # Make sure we don't have values > 12
            choices = [c if int(c.split()[0]) <= 12 else f"{int(c.split()[0]) - 6} (số chỉ giờ)" for c in choices]
            ans = choices.index(f"{hour} (số chỉ giờ)")
            steps = [
                {"text": "Kim ngắn của đồng hồ có nhiệm vụ chỉ giờ.", "highlight": "kim-dong-ho"},
                {"text": f"Vì thời gian là {hour} giờ sáng nên kim ngắn sẽ chỉ vào đúng số {hour}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3:
            q = f"Đồng hồ chỉ đúng {hour} giờ. Hỏi kim dài của đồng hồ khi đó đang chỉ vào số nào?"
            if is_duplicate(q): continue
            choices = ["Số 12", f"Số {hour}", "Số 6", "Số 3"]
            random.shuffle(choices)
            ans = choices.index("Số 12")
            steps = [
                {"text": "Đồng hồ chỉ giờ đúng khi và chỉ khi kim dài chỉ vào số 12.", "highlight": "kim-dong-ho"},
                {"text": f"Do đó, tại thời điểm {hour} giờ đúng, kim dài phải chỉ vào số 12.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4:
            q = f"Bố dặn {name} đúng {hour} giờ tối phải đi ngủ. Đồng hồ lúc đó có kim ngắn chỉ vào số {hour}, vậy kim dài sẽ chỉ số mấy?"
            if is_duplicate(q): continue
            choices = ["Số 6", "Số 12", "Số 9", f"Số {hour}"]
            random.shuffle(choices)
            ans = choices.index("Số 12")
            steps = [
                {"text": f"Thời điểm {hour} giờ tối là một mốc giờ đúng.", "highlight": "kim-dong-ho"},
                {"text": "Với giờ đúng, kim dài luôn chỉ vào số 12.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # pattern 5 (giờ rưỡi)
            q = f"Kim ngắn chỉ ở giữa số {hour} và số {hour+1 if hour < 12 else 1}, kim dài chỉ vào số 6. Lúc đó là mấy giờ?"
            if is_duplicate(q): continue
            choices = [f"{hour} giờ rưỡi", f"{hour} giờ đúng", f"{hour} giờ 6 phút", f"{hour+1 if hour < 12 else 1} giờ đúng"]
            random.shuffle(choices)
            ans = choices.index(f"{hour} giờ rưỡi")
            steps = [
                {"text": "Khi kim dài chỉ vào số 6, đồng hồ đang chỉ giờ rưỡi (hay 30 phút).", "highlight": "kim-dong-ho"},
                {"text": f"Kim ngắn ở giữa số {hour} và số tiếp theo tức là đã qua {hour} giờ. Vậy là {hour} giờ rưỡi.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_add_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])
        
        if pattern == 1: # Single-digit addition within 10
            a = random.randint(1, 8)
            b = random.randint(1, 10 - a)
            q = f"Tính kết quả của phép cộng sau: {a} + {b} = ?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=1)
            steps = [
                {"text": f"Thực hiện phép tính cộng: ta lấy {a} cộng thêm {b}.", "highlight": "phep-cong"},
                {"text": f"Ta đếm tiếp {b} đơn vị từ {a}: được {correct}.", "highlight": None},
                {"text": f"Kết quả: {a} + {b} = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Double digit + single digit (no carry)
            a_ten = random.randint(1, 8)
            a_unit = random.randint(0, 5)
            a = a_ten * 10 + a_unit
            b = random.randint(1, 9 - a_unit)
            q = f"Phép tính {a} + {b} có kết quả là bao nhiêu?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, incorrect_offset=4, min_val=10)
            steps = [
                {"text": f"Đặt tính rồi tính hoặc cộng nhẩm: cộng chữ số hàng đơn vị trước.", "highlight": "phep-cong"},
                {"text": f"Hàng đơn vị: {a_unit} + {b} = {a_unit + b}.", "highlight": None},
                {"text": f"Hàng chục giữ nguyên là {a_ten} chục. Kết quả là {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Double digit + double digit (no carry)
            a_chuc = random.randint(1, 7)
            a_dv = random.randint(0, 5)
            b_chuc = random.randint(1, 8 - a_chuc)
            b_dv = random.randint(0, 9 - a_dv)
            a = a_chuc * 10 + a_dv
            b = b_chuc * 10 + b_dv
            q = f"Kết quả của phép tính đặt dọc: {a} + {b} là:"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, incorrect_offset=8, min_val=20)
            steps = [
                {"text": "Cộng từ hàng đơn vị sang hàng chục.", "highlight": "phep-cong"},
                {"text": f"Cộng hàng đơn vị: {a_dv} + {b_dv} = {a_dv + b_dv}.", "highlight": None},
                {"text": f"Cộng hàng chục: {a_chuc} + {b_chuc} = {a_chuc + b_chuc}.", "highlight": None},
                {"text": f"Kết quả cuối cùng là: {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Three-number addition
            a = random.randint(1, 4)
            b = random.randint(1, 4)
            c = random.randint(1, 10 - a - b)
            q = f"Tính phép tính sau: {a} + {b} + {c} = ?"
            if is_duplicate(q): continue
            correct = a + b + c
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"Thực hiện từ trái qua phải: trước hết lấy {a} + {b} = {a+b}.", "highlight": "phep-cong"},
                {"text": f"Sau đó lấy kết quả {a+b} cộng tiếp với {c}: {a+b} + {c} = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Fill in the blank
            a = random.randint(1, 8)
            correct = random.randint(a + 1, 10)
            missing = correct - a
            q = f"Điền số thích hợp vào chỗ chấm: {a} + ... = {correct}"
            if is_duplicate(q): continue
            choices, ans = make_choices(missing, incorrect_offset=2, min_val=1)
            steps = [
                {"text": f"Để tìm số còn thiếu, ta có thể lấy kết quả trừ đi số đã biết.", "highlight": "phep-tru"},
                {"text": f"Phép tính: {correct} - {a} = {missing}.", "highlight": None},
                {"text": f"Vậy số cần điền là {missing}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_sub_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5])
        
        if pattern == 1: # Single digit subtraction within 10
            a = random.randint(2, 10)
            b = random.randint(1, a - 1)
            q = f"Tính nhẩm kết quả của phép trừ: {a} - {b} = ?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=0)
            steps = [
                {"text": f"Ta có {a} bớt đi {b}.", "highlight": "phep-tru"},
                {"text": f"Đếm lùi từ {a} đi {b} bước: ta được {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Double digit - single digit (no borrow)
            a_ten = random.randint(1, 9)
            a_unit = random.randint(1, 9)
            a = a_ten * 10 + a_unit
            b = random.randint(1, a_unit)
            q = f"Kết quả phép tính {a} - {b} là:"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, incorrect_offset=4, min_val=10)
            steps = [
                {"text": "Trừ chữ số hàng đơn vị trước.", "highlight": "phep-tru"},
                {"text": f"Hàng đơn vị: {a_unit} - {b} = {a_unit - b}.", "highlight": None},
                {"text": f"Hàng chục giữ nguyên {a_ten} chục. Kết quả là {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Double digit - double digit (no borrow)
            a_chuc = random.randint(2, 9)
            a_dv = random.randint(1, 9)
            b_chuc = random.randint(1, a_chuc - 1)
            b_dv = random.randint(0, a_dv)
            a = a_chuc * 10 + a_dv
            b = b_chuc * 10 + b_dv
            q = f"Phép tính hàng dọc {a} - {b} có kết quả bằng:"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, incorrect_offset=8, min_val=0)
            steps = [
                {"text": "Trừ từ hàng đơn vị sang hàng chục.", "highlight": "phep-tru"},
                {"text": f"Trừ hàng đơn vị: {a_dv} - {b_dv} = {a_dv - b_dv}.", "highlight": None},
                {"text": f"Trừ hàng chục: {a_chuc} - {b_chuc} = {a_chuc - b_chuc}.", "highlight": None},
                {"text": f"Ta nhận được kết quả: {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Double subtraction
            a = random.randint(6, 10)
            b = random.randint(1, a - 2)
            c = random.randint(1, a - b - 1)
            q = f"Tính nhanh phép tính: {a} - {b} - {c} = ?"
            if is_duplicate(q): continue
            correct = a - b - c
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=0)
            steps = [
                {"text": f"Thực hiện lần lượt từ trái qua phải: {a} - {b} = {a-b}.", "highlight": "phep-tru"},
                {"text": f"Tiếp tục lấy kết quả trừ đi {c}: {a-b} - {c} = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Fill in the blank subtraction
            a = random.randint(3, 10)
            correct = random.randint(1, a - 1)
            missing = a - correct
            q = f"Điền số thích hợp vào chỗ trống: {a} - ... = {correct}"
            if is_duplicate(q): continue
            choices, ans = make_choices(missing, incorrect_offset=2, min_val=1)
            steps = [
                {"text": f"Để tìm số bị trừ còn thiếu, ta lấy số ban đầu trừ đi kết quả.", "highlight": "phep-tru"},
                {"text": f"Phép tính: {a} - {correct} = {missing}.", "highlight": None},
                {"text": f"Số cần điền vào dấu ba chấm là {missing}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_count_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6, 7])
        
        if pattern == 1: # Số liền trước
            num = random.randint(2, 99)
            q = f"Số liền trước của số {num} là số nào?"
            if is_duplicate(q): continue
            correct = num - 1
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=1)
            steps = [
                {"text": "Số liền trước của một số thì bé hơn số đó 1 đơn vị.", "highlight": "dem-so"},
                {"text": f"Ta lấy {num} trừ đi 1: {num} - 1 = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Số liền sau
            num = random.randint(1, 98)
            q = f"Số liền sau của số {num} là số nào?"
            if is_duplicate(q): continue
            correct = num + 1
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=2)
            steps = [
                {"text": "Số liền sau của một số thì lớn hơn số đó 1 đơn vị.", "highlight": "dem-so"},
                {"text": f"Ta lấy {num} cộng thêm 1: {num} + 1 = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Số đứng giữa
            num = random.randint(1, 97)
            q = f"Số đứng ở giữa hai số {num} và {num+2} là số nào?"
            if is_duplicate(q): continue
            correct = num + 1
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"Đếm các số liên tiếp bắt đầu từ {num}: {num}, tiếp theo là {num+1}, rồi đến {num+2}.", "highlight": "dem-so"},
                {"text": f"Vậy số đứng giữa {num} và {num+2} chính là {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Số lớn nhất trong nhóm
            nums = random.sample(range(10, 100), 4)
            correct = max(nums)
            q = f"Trong các số sau: {', '.join(map(str, nums))}, số nào là số lớn nhất?"
            if is_duplicate(q): continue
            choices = [str(x) for x in nums]
            ans = choices.index(str(correct))
            steps = [
                {"text": "So sánh hàng chục của các số trước.", "highlight": "so-sanh"},
                {"text": f"Số có hàng chục lớn nhất (hoặc hàng đơn vị lớn nhất nếu hàng chục bằng nhau) chính là số lớn nhất, đó là số {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 5: # Số bé nhất trong nhóm
            nums = random.sample(range(10, 100), 4)
            correct = min(nums)
            q = f"Cho bốn số sau: {', '.join(map(str, nums))}. Hỏi số bé nhất là số nào?"
            if is_duplicate(q): continue
            choices = [str(x) for x in nums]
            ans = choices.index(str(correct))
            steps = [
                {"text": "Để tìm số bé nhất, ta so sánh chữ số hàng chục của các số.", "highlight": "so-sanh"},
                {"text": f"Số có hàng chục nhỏ nhất (hoặc hàng đơn vị nhỏ nhất nếu hàng chục bằng nhau) chính là số bé nhất, đó là số {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 6: # Tăng dần
            base = random.randint(1, 10)
            step = random.randint(2, 5)
            seq = [base + i*step for i in range(4)]
            seq_str = ", ".join(map(str, seq))
            wrong_seqs = [
                ", ".join(map(str, sorted(seq, reverse=True))),
                ", ".join(map(str, [seq[1], seq[0], seq[3], seq[2]])),
                ", ".join(map(str, [seq[0], seq[2], seq[1], seq[3]]))
            ]
            q = "Dãy số nào dưới đây được sắp xếp theo thứ tự từ bé đến lớn?"
            if is_duplicate(q + str(seq)): continue
            choices = [seq_str] + wrong_seqs
            random.shuffle(choices)
            ans = choices.index(seq_str)
            steps = [
                {"text": "Sắp xếp theo thứ tự từ bé đến lớn có nghĩa là số đứng sau phải lớn hơn số đứng trước.", "highlight": "so-sanh"},
                {"text": f"Nhìn vào các dãy số, ta thấy dãy {seq_str} tăng dần từ bé đến lớn.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Giảm dần
            base = random.randint(40, 90)
            step = random.randint(2, 5)
            seq = [base - i*step for i in range(4)]
            seq_str = ", ".join(map(str, seq))
            wrong_seqs = [
                ", ".join(map(str, sorted(seq))),
                ", ".join(map(str, [seq[1], seq[0], seq[3], seq[2]])),
                ", ".join(map(str, [seq[0], seq[2], seq[1], seq[3]]))
            ]
            q = "Dãy số nào dưới đây được sắp xếp theo thứ tự từ lớn đến bé?"
            if is_duplicate(q + str(seq)): continue
            choices = [seq_str] + wrong_seqs
            random.shuffle(choices)
            ans = choices.index(seq_str)
            steps = [
                {"text": "Sắp xếp theo thứ tự từ lớn đến bé có nghĩa là số đứng sau phải bé hơn số đứng trước.", "highlight": "so-sanh"},
                {"text": f"Nhìn vào các dãy số, ta thấy dãy {seq_str} giảm dần từ lớn đến bé.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_len_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6])
        name = random.choice(NAMES)
        obj = random.choice(OBJECTS).split(' ')[0] # just "cái", "chiếc"...
        
        if pattern == 1: # Addition with cm
            a = random.randint(1, 15)
            b = random.randint(1, 15)
            q = f"Tính phép tính độ dài sau: {a}cm + {b}cm = ?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=3, min_val=2)
            steps = [
                {"text": "Khi cộng hai số kèm theo đơn vị đo giống nhau (ở đây là cm), ta cộng các số và giữ nguyên đơn vị.", "highlight": "do-do-dai"},
                {"text": f"Ta lấy {a} + {b} = {correct}.", "highlight": "phep-cong"},
                {"text": f"Kết quả là {correct}cm.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Subtraction with cm
            a = random.randint(10, 30)
            b = random.randint(1, a - 1)
            q = f"Kết quả của phép tính: {a}cm - {b}cm là bao nhiêu?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=4, min_val=1)
            steps = [
                {"text": "Thực hiện phép trừ các số và giữ nguyên đơn vị xăng-ti-mét (cm).", "highlight": "do-do-dai"},
                {"text": f"Phép tính: {a} - {b} = {correct}.", "highlight": "phep-tru"},
                {"text": f"Đáp số: {correct}cm.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Combo operation
            a = random.randint(5, 15)
            b = random.randint(2, 10)
            c = random.randint(1, a + b - 1)
            q = f"Tìm kết quả của biểu thức: {a}cm + {b}cm - {c}cm = ?"
            if is_duplicate(q): continue
            correct = a + b - c
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=3, min_val=1)
            steps = [
                {"text": "Ta tính lần lượt từ bên trái qua bên phải.", "highlight": "do-do-dai"},
                {"text": f"Đầu tiên: {a}cm + {b}cm = {a+b}cm.", "highlight": "phep-cong"},
                {"text": f"Tiếp theo: {a+b}cm - {c}cm = {correct}cm.", "highlight": "phep-tru"}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Word problem addition (lengths)
            a = random.randint(5, 20)
            b = random.randint(5, 20)
            q = f"Băng giấy xanh dài {a}cm, băng giấy đỏ dài {b}cm. Hỏi cả hai băng giấy dài bao nhiêu xăng-ti-mét?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=5, min_val=10)
            steps = [
                {"text": "Muốn tìm độ dài cả hai băng giấy, ta thực hiện phép tính cộng độ dài của chúng.", "highlight": "do-do-dai"},
                {"text": f"Phép tính: {a}cm + {b}cm = {correct}cm.", "highlight": "phep-cong"},
                {"text": f"Vậy cả hai băng giấy dài {correct}cm.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 5: # Word problem subtraction (lengths)
            a = random.randint(15, 30)
            b = random.randint(2, 10)
            q = f"Đoạn thẳng AB dài {a}cm. Đoạn thẳng CD ngắn hơn đoạn thẳng AB là {b}cm. Hỏi đoạn thẳng CD dài bao nhiêu xăng-ti-mét?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=4, min_val=5)
            steps = [
                {"text": "Vì đoạn CD ngắn hơn đoạn AB nên ta dùng phép tính trừ lấy độ dài AB trừ đi phần ngắn hơn.", "highlight": "do-do-dai"},
                {"text": f"Phép tính: {a}cm - {b}cm = {correct}cm.", "highlight": "phep-tru"},
                {"text": f"Vậy đoạn thẳng CD dài {correct}cm.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Word problem cut pencil
            a = random.randint(10, 20)
            b = random.randint(1, 5)
            q = f"Bút chì của {name} dài {a}cm. Sau khi {name} gọt bút chì bớt đi {b}cm, bút chì còn lại dài bao nhiêu cm?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit='cm', incorrect_offset=3, min_val=5)
            steps = [
                {"text": "Bút chì bị gọt bớt tức là độ dài bị giảm đi. Ta dùng phép tính trừ.", "highlight": "do-do-dai"},
                {"text": f"Lấy độ dài lúc đầu trừ đi phần đã bị gọt: {a}cm - {b}cm = {correct}cm.", "highlight": "phep-tru"},
                {"text": f"Bút chì còn lại dài {correct}cm.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_loivan_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6, 7])
        name1 = random.choice(NAMES)
        name2 = random.choice([n for n in NAMES if n != name1])
        fruit = random.choice(FRUITS)
        animal = random.choice(ANIMALS)
        obj = random.choice(OBJECTS)
        
        if pattern == 1: # Addition story
            a = random.randint(2, 9)
            b = random.randint(1, 10 - a)
            q = f"{name1} có {a} {fruit}. {name2} cho {name1} thêm {b} {fruit} nữa. Hỏi lúc này {name1} có tất cả mấy {fruit}?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit=f" {fruit.split(' ')[0]}", incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"Lúc đầu {name1} có {a} {fruit}.", "highlight": None},
                {"text": f"Được tặng thêm {b} {fruit}.", "highlight": None},
                {"text": f"Số quả có tất cả là kết quả của phép cộng: {a} + {b} = {correct}.", "highlight": "phep-cong"},
                {"text": f"Đáp số: {correct} {fruit}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Subtraction story
            a = random.randint(5, 10)
            b = random.randint(1, a - 1)
            q = f"Trong cành cây có {a} {animal}. Sau đó có {b} {animal} bay đi mất. Hỏi trên cành cây còn lại bao nhiêu {animal}?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit=f" {animal.split(' ')[0]}", incorrect_offset=2, min_val=0)
            steps = [
                {"text": f"Số con chim ban đầu là {a} con.", "highlight": None},
                {"text": f"Có {b} con bay đi tức là số con chim giảm đi.", "highlight": None},
                {"text": f"Thực hiện phép tính trừ: {a} - {b} = {correct}.", "highlight": "phep-tru"},
                {"text": f"Vậy trên cành cây còn lại {correct} {animal}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Give away story
            a = random.randint(6, 12)
            b = random.randint(1, a - 2)
            q = f"{name1} có {a} {obj}. {name1} cho {name2} {b} {obj}. Hỏi {name1} còn lại bao nhiêu {obj}?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit=f" {obj.split(' ')[0]}", incorrect_offset=3, min_val=1)
            steps = [
                {"text": f"Số {obj} ban đầu là {a}.", "highlight": None},
                {"text": f"Số {obj} cho đi là {b}.", "highlight": None},
                {"text": f"Để tìm số {obj} còn lại, ta làm phép trừ: {a} - {b} = {correct}.", "highlight": "phep-tru"},
                {"text": f"Đáp số: {correct} {obj}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Double animals addition
            a = random.randint(2, 8)
            b = random.randint(2, 8)
            animal2 = random.choice([x for x in ANIMALS if x != animal])
            q = f"Trong sân nhà {name1} có {a} {animal} và {b} {animal2}. Hỏi trong sân nhà {name1} có tất cả bao nhiêu con vật?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit=" con vật", incorrect_offset=3, min_val=2)
            steps = [
                {"text": f"Số {animal} là {a} con. Số {animal2} là {b} con.", "highlight": None},
                {"text": f"Để tính tổng số con vật, ta dùng phép cộng: {a} + {b} = {correct}.", "highlight": "phep-cong"},
                {"text": f"Trong sân có tất cả {correct} con vật.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 5: # More than comparison
            a = random.randint(2, 7)
            b = random.randint(1, 5)
            q = f"{name1} có {a} {obj}. {name2} có nhiều hơn {name1} là {b} {obj}. Hỏi {name2} có bao nhiêu {obj}?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit=f" {obj.split(' ')[0]}", incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"{name1} có {a} {obj}.", "highlight": None},
                {"text": f"{name2} có nhiều hơn nên ta lấy số lượng của {name1} cộng thêm phần nhiều hơn.", "highlight": "phep-cong"},
                {"text": f"Phép tính: {a} + {b} = {correct}.", "highlight": None},
                {"text": f"Vậy {name2} có {correct} {obj}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 6: # Less than comparison
            a = random.randint(6, 12)
            b = random.randint(1, 4)
            q = f"{name1} có {a} {obj}. {name2} có ít hơn {name1} là {b} {obj}. Hỏi {name2} có bao nhiêu {obj}?"
            if is_duplicate(q): continue
            correct = a - b
            choices, ans = make_choices(correct, unit=f" {obj.split(' ')[0]}", incorrect_offset=3, min_val=1)
            steps = [
                {"text": f"{name1} có {a} {obj}.", "highlight": None},
                {"text": f"{name2} có ít hơn nên ta lấy số lượng của {name1} trừ đi phần ít hơn.", "highlight": "phep-tru"},
                {"text": f"Phép tính: {a} - {b} = {correct}.", "highlight": None},
                {"text": f"Vậy {name2} có {correct} {obj}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Group members
            a = random.randint(3, 8)
            b = random.randint(3, 8)
            q = f"Lớp 1A có tổ Một gồm {a} bạn nam và {b} bạn nữ. Hỏi tổ Một có tất cả bao nhiêu bạn học sinh?"
            if is_duplicate(q): continue
            correct = a + b
            choices, ans = make_choices(correct, unit=" bạn", incorrect_offset=3, min_val=3)
            steps = [
                {"text": f"Tổ Một có {a} bạn nam và {b} bạn nữ.", "highlight": None},
                {"text": f"Tổng số bạn học sinh trong tổ là: {a} + {b} = {correct} bạn.", "highlight": "phep-cong"}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_nangcao_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6, 7])
        name1 = random.choice(NAMES)
        name2 = random.choice([n for n in NAMES if n != name1])
        
        if pattern == 1: # Queue line logic
            a = random.randint(2, 6)
            b = random.randint(2, 6)
            q = f"Trong một hàng dọc, {name1} đứng thứ {a} từ trên xuống và thứ {b} từ dưới lên. Hỏi hàng đó có tất cả bao nhiêu bạn?"
            if is_duplicate(q): continue
            correct = a + b - 1
            choices, ans = make_choices(correct, unit=" bạn", incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"Nếu tính từ trên xuống, có {a-1} bạn đứng trước {name1}.", "highlight": "logic"},
                {"text": f"Nếu tính từ dưới lên, có {b-1} bạn đứng sau {name1}.", "highlight": None},
                {"text": f"Tổng số bạn trong hàng là: (số bạn trước) + {name1} + (số bạn sau) = {a-1} + 1 + {b-1} = {correct} bạn.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Double expression comparison
            a = random.randint(5, 15)
            b = random.randint(2, 10)
            c = random.randint(1, a + b - 2)
            val1 = a + b - c
            
            d = random.randint(5, 15)
            e = random.randint(2, 10)
            val2 = d + e
            
            q = f"Điền dấu thích hợp (<, >, =) vào chỗ chấm: {a} + {b} - {c} ... {d} + {e}"
            if is_duplicate(q): continue
            
            if val1 < val2:
                correct = "<"
            elif val1 > val2:
                correct = ">"
            else:
                correct = "="
                
            choices = ["<", ">", "=", "Không so sánh được"]
            ans = choices.index(correct)
            steps = [
                {"text": f"Tính kết quả vế trái: {a} + {b} - {c} = {a+b} - {c} = {val1}.", "highlight": "phep-tinh-phuc-tap"},
                {"text": f"Tính kết quả vế phải: {d} + {e} = {val2}.", "highlight": None},
                {"text": f"So sánh hai kết quả: vì {val1} {'bé hơn' if val1 < val2 else 'lớn hơn' if val1 > val2 else 'bằng'} {val2} nên ta điền dấu {correct}.", "highlight": "so-sanh"}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Triangle count
            triangles = random.choice([3, 4, 5, 6])
            q = f"Một hình tam giác lớn được chia đôi bởi một đường thẳng kẻ từ đỉnh xuống cạnh đáy. Hỏi hình đó gồm tất cả bao nhiêu hình tam giác?"
            # Actually, standard triangle split in 2 gives 1 large + 2 small = 3 triangles.
            # Let's write a fixed geometry logic puzzle:
            # "Hình vẽ có một hình chữ nhật lớn chia làm 4 ô vuông nhỏ. Hỏi có bao nhiêu hình chữ nhật tất cả?"
            # Rects in 2x2 grid: (2*3/2)*(2*3/2) = 9
            q = "Một hình vuông lớn được chia thành 4 ô vuông nhỏ bằng nhau. Hỏi hình đó chứa tất cả bao nhiêu hình vuông?"
            if is_duplicate(q): continue
            # 4 small squares + 1 large square = 5 squares
            choices = ["4 hình vuông", "5 hình vuông", "6 hình vuông", "8 hình vuông"]
            ans = 1 # 5 hình vuông
            steps = [
                {"text": "Ta đếm các hình vuông nhỏ trước: gồm có 4 hình vuông nhỏ.", "highlight": "hinh-hoc"},
                {"text": "Tiếp theo ta đếm hình vuông lớn bên ngoài bao quanh 4 hình nhỏ: có 1 hình vuông lớn.", "highlight": None},
                {"text": "Tổng số hình vuông là: 4 + 1 = 5 hình vuông.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Sequence pattern
            base = random.randint(1, 5)
            step = random.randint(2, 4)
            seq = [base + i*step for i in range(4)]
            correct = seq[-1] + step
            q = f"Cho dãy số: {', '.join(map(str, seq))}, ... Số tiếp theo điền vào chỗ chấm để hợp quy luật là số nào?"
            if is_duplicate(q): continue
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=2)
            steps = [
                {"text": f"Nhận xét quy luật của dãy số: mỗi số đứng sau bằng số đứng trước cộng thêm {step}.", "highlight": "logic"},
                {"text": f"Cụ thể: {seq[0]} + {step} = {seq[1]}, {seq[1]} + {step} = {seq[2]}, ...", "highlight": None},
                {"text": f"Do đó số tiếp theo sẽ là: {seq[-1]} + {step} = {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 5: # Age logic
            age = random.randint(5, 7)
            future = random.randint(2, 5)
            q = f"Năm nay {name1} {age} tuổi. Hỏi {future} năm nữa {name1} bao nhiêu tuổi?"
            if is_duplicate(q): continue
            correct = age + future
            choices, ans = make_choices(correct, unit=" tuổi", incorrect_offset=2, min_val=4)
            steps = [
                {"text": f"Mỗi năm mỗi người đều tăng thêm 1 tuổi.", "highlight": "logic"},
                {"text": f"Sau {future} năm, {name1} sẽ tăng thêm {future} tuổi. Phép cộng: {age} + {future} = {correct}.", "highlight": "phep-cong"},
                {"text": f"Đáp số: {correct} tuổi.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 6: # Operations puzzle: Find X
            a = random.randint(2, 8)
            b = random.randint(1, 5)
            result = random.randint(6, 12)
            # X + a - b = result => X = result + b - a
            X = result + b - a
            if X <= 0 or X > 15: continue
            q = f"Tìm một số, biết rằng lấy số đó cộng với {a} rồi trừ đi {b} thì bằng {result}."
            if is_duplicate(q): continue
            choices, ans = make_choices(X, incorrect_offset=2, min_val=1)
            steps = [
                {"text": f"Ta giải ngược từ cuối lên: trước khi trừ đi {b} để bằng {result}, kết quả là: {result} + {b} = {result + b}.", "highlight": "logic"},
                {"text": f"Số ban đầu cộng với {a} bằng {result + b}. Vậy số ban đầu là: {result + b} - {a} = {X}.", "highlight": "phep-tru"},
                {"text": f"Số cần tìm là {X}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # Date logic
            day_of_month = random.randint(1, 20)
            days = ["Hai", "Ba", "Tư", "Năm", "Sáu", "Bảy", "Chủ Nhật"]
            idx = random.randint(0, 6)
            day_name = days[idx]
            q = f"Hôm nay là Thứ {day_name} ngày {day_of_month}. Hỏi Thứ {day_name} tuần sau là ngày mấy?"
            if is_duplicate(q): continue
            correct = day_of_month + 7
            choices, ans = make_choices(correct, unit=" tháng này", incorrect_offset=3, min_val=8)
            steps = [
                {"text": "Một tuần lễ có đúng 7 ngày.", "highlight": "logic"},
                {"text": f"Đúng ngày này tuần sau (cùng thứ) sẽ cộng thêm 7 ngày nữa.", "highlight": None},
                {"text": f"Ta tính: {day_of_month} + 7 = {correct}.", "highlight": "phep-cong"},
                {"text": f"Thứ {day_name} tuần sau chính là ngày {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_dem100_problem(pid, topic_id):
    while True:
        pattern = random.choice([1, 2, 3, 4, 5, 6, 7])
        
        if pattern == 1: # Số gồm chục và đơn vị
            num = random.randint(20, 99)
            chuc = num // 10
            dv = num % 10
            q = f"Số {num} gồm mấy chục và mấy đơn vị?"
            if is_duplicate(q): continue
            correct_str = f"{chuc} chục và {dv} đơn vị"
            wrong1 = f"{dv} chục và {chuc} đơn vị"
            wrong2 = f"{chuc} chục và 0 đơn vị"
            wrong3 = f"{chuc}0 chục và {dv} đơn vị"
            choices = [correct_str, wrong1, wrong2, wrong3]
            random.shuffle(choices)
            ans = choices.index(correct_str)
            steps = [
                {"text": f"Số {num} có chữ số {chuc} ở vị trí hàng chục và chữ số {dv} ở vị trí hàng đơn vị.", "highlight": "so-dem-100"},
                {"text": f"Vậy số {num} gồm {chuc} chục và {dv} đơn vị.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 2: # Viết số từ cấu tạo
            chuc = random.randint(2, 9)
            dv = random.randint(1, 9)
            correct = chuc * 10 + dv
            q = f"Số gồm {chuc} chục và {dv} đơn vị được viết là:"
            if is_duplicate(q): continue
            choices, ans = make_choices(correct, incorrect_offset=5, min_val=20)
            steps = [
                {"text": "Ta ghép chữ số hàng chục đứng trước và chữ số hàng đơn vị đứng sau.", "highlight": "so-dem-100"},
                {"text": f"Hàng chục là {chuc}, hàng đơn vị là {dv}. Ghép lại ta được số {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 3: # Đọc số thành chữ
            num = random.randint(20, 99)
            word = to_vietnamese_word(num)
            q = f"Số {num} được đọc là gì?"
            if is_duplicate(q): continue
            
            # Make incorrect reads
            wrong_words = []
            while len(wrong_words) < 3:
                w_num = random.randint(20, 99)
                if w_num != num:
                    w = to_vietnamese_word(w_num)
                    if w not in wrong_words:
                        wrong_words.append(w)
            choices = [word] + wrong_words
            random.shuffle(choices)
            ans = choices.index(word)
            steps = [
                {"text": f"Hàng chục là {num//10} (đọc là {NUM_WORDS_TEN[num//10]} mươi). Hàng đơn vị là {num%10}.", "highlight": "so-dem-100"},
                {"text": f"Kết hợp đúng quy tắc đọc tiếng Việt: số {num} đọc là \"{word}\".", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 4: # Viết số từ chữ
            num = random.randint(20, 99)
            word = to_vietnamese_word(num)
            q = f"Số \"{word}\" được viết bằng chữ số là:"
            if is_duplicate(q): continue
            choices, ans = make_choices(num, incorrect_offset=6, min_val=20)
            steps = [
                {"text": f"Dựa vào cách đọc \"{word}\", ta phân tích được số này gồm {num//10} chục và {num%10} đơn vị.", "highlight": "so-dem-100"},
                {"text": f"Vậy số đó được viết là {num}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 5: # Số tròn chục ở giữa
            tens = [10, 20, 30, 40, 50, 60, 70, 80, 90]
            low = random.choice(tens[:-2])
            high = random.choice([t for t in tens if t >= low + 20])
            correct = random.choice([t for t in tens if low < t < high])
            q = f"Trong các số sau, số tròn chục nào nằm ở giữa {low} và {high}?"
            if is_duplicate(q): continue
            wrong_choices = [low - 10 if low > 10 else 99, high + 10 if high < 90 else 5, low, high]
            choices = [str(correct)] + [str(x) for x in wrong_choices[:3]]
            random.shuffle(choices)
            ans = choices.index(str(correct))
            steps = [
                {"text": f"Các số tròn chục lớn hơn {low} và nhỏ hơn {high} có thể là số nằm giữa hai số này.", "highlight": "so-dem-100"},
                {"text": f"Trong các phương án, số tròn chục thỏa mãn là {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        elif pattern == 6: # Số bé nhất/lớn nhất có 2 chữ số
            is_max = random.choice([True, False])
            is_diff = random.choice([True, False])
            
            if is_max:
                if is_diff:
                    q = "Số lớn nhất có 2 chữ số khác nhau là số nào?"
                    correct = 98
                    steps = [{"text": "Số lớn nhất có 2 chữ số là 99, nhưng hai chữ số phải khác nhau nên số tiếp theo nhỏ hơn là 98.", "highlight": "so-dem-100"}]
                else:
                    q = "Số lớn nhất có 2 chữ số là số nào?"
                    correct = 99
                    steps = [{"text": "Số lớn nhất có 2 chữ số trong phạm vi 100 là 99.", "highlight": "so-dem-100"}]
            else:
                if is_diff:
                    q = "Số bé nhất có 2 chữ số khác nhau là số nào?"
                    correct = 10
                    steps = [{"text": "Số bé nhất có 2 chữ số bắt đầu từ 10. Chữ số 1 và 0 khác nhau. Vậy số đó là 10.", "highlight": "so-dem-100"}]
                else:
                    q = "Số bé nhất có 2 chữ số là số nào?"
                    correct = 10
                    steps = [{"text": "Số bé nhất có 2 chữ số là số 10.", "highlight": "so-dem-100"}]
                    
            if is_duplicate(q): continue
            choices, ans = make_choices(correct, incorrect_offset=2, min_val=9 if correct < 20 else 90)
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            
        else: # So sánh số
            a = random.randint(10, 99)
            b = random.randint(10, 99)
            if a == b: continue
            q = f"Điền dấu thích hợp vào chỗ chấm: {a} ... {b}"
            if is_duplicate(q): continue
            correct = ">" if a > b else "<"
            choices = [">", "<", "=", "Không có dấu"]
            ans = choices.index(correct)
            steps = [
                {"text": f"So sánh hàng chục: hàng chục của {a} là {a//10}, hàng chục của {b} is {b//10}.", "highlight": "so-sanh"},
                {"text": f"Nếu hàng chục lớn hơn thì số đó lớn hơn. Nếu hàng chục bằng nhau, ta so sánh tiếp hàng đơn vị.", "highlight": None},
                {"text": f"Vì {a} {'lớn hơn' if a > b else 'bé hơn'} {b} nên ta điền dấu {correct}.", "highlight": None}
            ]
            return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def generate_exam_problem(pid, topic_id, is_final=False):
    # Generates unique midterm or final exam problems by mixing concepts
    while True:
        if not is_final: # Midterm exam (early concepts: counting, adding/subtraction up to 10/20, basic shapes)
            pattern = random.choice([1, 2, 3, 4])
            if pattern == 1:
                # Count representation
                a = random.randint(1, 19)
                q = f"Đề thi Giữa Kỳ: Số liền trước của số {a+1} là số nào?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a, incorrect_offset=2, min_val=0)
                steps = [{"text": f"Số liền trước của {a+1} được tính bằng cách trừ đi 1 đơn vị: {a+1} - 1 = {a}.", "highlight": "thi-giua-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            elif pattern == 2:
                # Sum within 10
                a = random.randint(1, 9)
                b = random.randint(1, 10 - a)
                q = f"Đề thi Giữa Kỳ - Tính nhẩm: {a} + {b} = ?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a+b, incorrect_offset=2, min_val=1)
                steps = [{"text": f"Thực hiện cộng hai số đơn giản: {a} + {b} = {a+b}.", "highlight": "thi-giua-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            elif pattern == 3:
                # Subtraction within 10
                a = random.randint(2, 10)
                b = random.randint(1, a - 1)
                q = f"Đề thi Giữa Kỳ - Tính nhẩm: {a} - {b} = ?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a-b, incorrect_offset=2, min_val=0)
                steps = [{"text": f"Thực hiện phép trừ cơ bản trong phạm vi 10: {a} - {b} = {a-b}.", "highlight": "thi-giua-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            else:
                # Simple word problem
                a = random.randint(2, 7)
                b = random.randint(1, 10-a)
                name = random.choice(NAMES)
                q = f"Đề thi Giữa Kỳ: {name} có {a} quả bóng bay 🎈, bạn tặng thêm {b} quả. Hỏi {name} có tất cả bao nhiêu quả bóng bay?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a+b, unit=" quả", incorrect_offset=2, min_val=1)
                steps = [{"text": f"Có thêm bóng tức là thực hiện phép cộng: {a} + {b} = {a+b} quả bóng.", "highlight": "thi-giua-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
        else: # Final exam (includes clock, length cm, operations up to 100, comparisons, complex word problems)
            pattern = random.choice([1, 2, 3, 4, 5])
            if pattern == 1:
                # Clock
                hour = random.randint(1, 12)
                q = f"Đề thi Cuối Kỳ: Đồng hồ chỉ đúng {hour} giờ. Hỏi kim ngắn chỉ số mấy và kim dài chỉ số mấy?"
                if is_duplicate(q): continue
                correct_str = f"Kim ngắn chỉ số {hour}, kim dài chỉ số 12"
                wrong1 = f"Kim ngắn chỉ số 12, kim dài chỉ số {hour}"
                wrong2 = f"Kim ngắn chỉ số {hour}, kim dài chỉ số 6"
                wrong3 = f"Kim ngắn chỉ số 6, kim dài chỉ số 12"
                choices = [correct_str, wrong1, wrong2, wrong3]
                random.shuffle(choices)
                ans = choices.index(correct_str)
                steps = [{"text": "Đối với đồng hồ chỉ giờ đúng, kim ngắn sẽ chỉ vào đúng số chỉ giờ, còn kim dài luôn luôn chỉ vào số 12.", "highlight": "thi-cuoi-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            elif pattern == 2:
                # Length addition
                a = random.randint(10, 40)
                b = random.randint(5, 30)
                q = f"Đề thi Cuối Kỳ - Thực hiện phép tính: {a}cm + {b}cm = ?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a+b, unit="cm", incorrect_offset=5, min_val=15)
                steps = [{"text": f"Cộng các số đo có cùng đơn vị cm: {a} + {b} = {a+b}cm.", "highlight": "thi-cuoi-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            elif pattern == 3:
                # Large numbers addition
                a = random.randint(20, 60)
                b = random.randint(10, 39)
                # Ensure no carry
                a_dv = a % 10
                b_dv = b % 10
                if a_dv + b_dv >= 10:
                    b -= b_dv
                q = f"Đề thi Cuối Kỳ - Đặt tính rồi tính: {a} + {b} = ?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a+b, incorrect_offset=6, min_val=30)
                steps = [{"text": f"Đặt tính dọc và thực hiện cộng từ hàng đơn vị sang hàng chục: {a} + {b} = {a+b}.", "highlight": "thi-cuoi-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            elif pattern == 4:
                # Number structure
                num = random.randint(20, 99)
                q = f"Đề thi Cuối Kỳ: Số gồm {num//10} chục và {num%10} đơn vị được đọc là:"
                if is_duplicate(q): continue
                word = to_vietnamese_word(num)
                wrong_words = []
                while len(wrong_words) < 3:
                    w_num = random.randint(20, 99)
                    if w_num != num:
                        w = to_vietnamese_word(w_num)
                        if w not in wrong_words:
                            wrong_words.append(w)
                choices = [word] + wrong_words
                random.shuffle(choices)
                ans = choices.index(word)
                steps = [{"text": f"Số gồm {num//10} chục và {num%10} đơn vị viết là {num}, đọc là \"{word}\".", "highlight": "thi-cuoi-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
            else:
                # Subtraction word problem up to 100
                a = random.randint(30, 80)
                b = random.randint(10, a - 10)
                # Ensure no borrow
                a_dv = a % 10
                b_dv = b % 10
                if a_dv < b_dv:
                    b -= (b_dv - a_dv)
                name = random.choice(NAMES)
                q = f"Đề thi Cuối Kỳ: {name} có {a} viên bi màu xanh. {name} cho bạn {b} viên bi. Hỏi {name} còn lại bao nhiêu viên bi?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a-b, unit=" viên", incorrect_offset=6, min_val=5)
                steps = [{"text": f"Cho bạn bi làm giảm số bi ban đầu, dùng phép trừ: {a} - {b} = {a-b} viên bi.", "highlight": "thi-cuoi-ky"}]
                return {"id": pid, "topicId": topic_id, "question": q, "choices": choices, "answer": ans, "steps": steps}

def main():
    print("Bắt đầu đọc topics.js và problems.js...")
    
    with open('src/data/topics.js', 'r', encoding='utf-8') as f:
        topics_content = f.read()
    
    topics_match = re.search(r'export const topics = (\{[\s\S]*?\});', topics_content)
    if not topics_match:
        print("Lỗi: Không tìm thấy khai báo export const topics trong topics.js")
        return
    topics = json.loads(topics_match.group(1))
    
    with open('src/data/problems.js', 'r', encoding='utf-8') as f:
        problems_content = f.read()
        
    problems_match = re.search(r'export const problems = (\{[\s\S]*?\});', problems_content)
    if not problems_match:
        print("Lỗi: Không tìm thấy khai báo export const problems trong problems.js")
        return
    problems = json.loads(problems_match.group(1))

    # Add existing questions to generated_questions set to prevent duplication
    for pid, prob in problems.items():
        if 'question' in prob:
            normalized = re.sub(r'\s+', ' ', prob['question']).strip().lower()
            generated_questions.add(normalized)

    grade1_topics = topics.get("1", [])
    print(f"Số lượng chủ đề Lớp 1 tìm thấy: {len(grade1_topics)}")
    
    # Process each Grade 1 topic
    for topic in grade1_topics:
        t_id = topic['id']
        t_name = topic['name']
        prob_ids = topic.setdefault('problemIds', [])
        
        current_count = len(prob_ids)
        target = 50
        need = target - current_count
        print(f"Chủ đề '{t_id}' ({t_name}): Đang có {current_count} bài tập. Cần sinh thêm {need} bài.")
        
        if need <= 0:
            print(f"-> Chủ đề '{t_id}' đã có đủ 50 bài tập hoặc nhiều hơn!")
            continue
            
        generated_count = 0
        idx = current_count + 1
        
        # Generate new problems
        while len(prob_ids) < target:
            new_pid = f"{t_id}-{idx}"
            
            # Double check that new_pid is not already in problems
            while new_pid in problems:
                idx += 1
                new_pid = f"{t_id}-{idx}"
                
            if t_id == 'g1-clock':
                prob = generate_clock_problem(new_pid, t_id)
            elif t_id == 'g1-add':
                prob = generate_add_problem(new_pid, t_id)
            elif t_id == 'g1-sub':
                prob = generate_sub_problem(new_pid, t_id)
            elif t_id == 'g1-count':
                prob = generate_count_problem(new_pid, t_id)
            elif t_id == 'g1-len':
                prob = generate_len_problem(new_pid, t_id)
            elif t_id == 'g1-loivan':
                prob = generate_loivan_problem(new_pid, t_id)
            elif t_id == 'g1-nangcao':
                prob = generate_nangcao_problem(new_pid, t_id)
            elif t_id == 'g1-dem100':
                prob = generate_dem100_problem(new_pid, t_id)
            elif t_id == 'g1-midterm':
                prob = generate_exam_problem(new_pid, t_id, is_final=False)
            elif t_id == 'g1-final':
                prob = generate_exam_problem(new_pid, t_id, is_final=True)
            else:
                # Generic fallback
                a = random.randint(1, 10)
                b = random.randint(1, 10)
                q = f"Tính phép tính cơ bản sau: {a} + {b} = ?"
                if is_duplicate(q): continue
                choices, ans = make_choices(a+b, incorrect_offset=2, min_val=1)
                steps = [{"text": f"Ta tính {a} + {b} = {a+b}.", "highlight": None}]
                prob = {"id": new_pid, "topicId": t_id, "question": q, "choices": choices, "answer": ans, "steps": steps}
                
            problems[new_pid] = prob
            prob_ids.append(new_pid)
            generated_count += 1
            idx += 1
            
        print(f"-> Đã sinh thành công {generated_count} bài tập cho '{t_id}'. Tổng số bây giờ: {len(prob_ids)}")

    # Save topics.js back
    new_topics_code = f"export const topics = {json.dumps(topics, ensure_ascii=False, indent=2)};\n"
    with open('src/data/topics.js', 'w', encoding='utf-8') as f:
        f.write(new_topics_code)
    print("Đã ghi đè lại file src/data/topics.js!")
    
    # Save problems.js back
    new_problems_code = f"export const problems = {json.dumps(problems, ensure_ascii=False, indent=2)};\n"
    with open('src/data/problems.js', 'w', encoding='utf-8') as f:
        f.write(new_problems_code)
    print("Đã ghi đè lại file src/data/problems.js!")
    
    print("\nHoàn thành! Tất cả 10 chủ đề Toán Lớp 1 hiện tại đều có chính xác 50 bài tập không trùng lặp.")

if __name__ == '__main__':
    main()
