import re
def has_choice_marker(text):
    return bool(re.search(r'(?:^|\s)[A-D][\.\)]', text))

t = 'A.\xa016/03/2025.\tB.\xa003/16/2025.\t   C.\xa003/16/25.    \t    D.\xa016/03/25'
print(f"Result: {has_choice_marker(t)}")
m = re.search(r'(?:^|\s)[A-D][\.\)]', t)
if m: print(f"Match: [{m.group()}]")
