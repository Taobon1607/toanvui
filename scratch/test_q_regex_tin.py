import re
def is_question_start(text):
    return bool(re.match(r'^(?:Câu|Question|Q|(\d+))\s*\d*[\.\:\)]\s*', text, re.I))

t = 'A.\xa016/03/2025.\tB.\xa003/16/2025.\t   C.\xa003/16/25.    \t    D.\xa016/03/25'
print(f"Result: {is_question_start(t)}")
