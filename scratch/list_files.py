import os, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
folder = 'E:\\toanvui-main\\Đề cương ôn thi lớp 7'
for f in os.listdir(folder):
    print(repr(f))
