'''
zh_cn(简体中文):
参数	            功能	                        示例
--f <文件路径>	    直接指定Brainfuck代码文件	    --f hello.bf
--speed <秒数>	    调整执行速度(默认0.1秒)	       --speed 0.5
--mem <行>x<列>	    自定义二维内存尺寸(默认10x12)   --mem 20x16
--en                英文模式                      --en

en(英文):
parameters	        function	                                    Example
--f <File path>      Specify the Brainfuck code file directly	    --f hello.bf
--speed <seconds>	Adjust execution speed (default 0.1 seconds)	--speed 0.5
--mem <row>x<column> Customize 2D memory size (default 10x12)       --mem 20x16
--en                 English model                                  --en
'''
import os
import sys
import time
import tkinter as tk
from tkinter import filedialog

def reset_output(print_list):
    global memory_wide,memory_long,memory
    os.system('cls' if os.name == 'nt' else 'clear')
    print("Memory:")
    for i in range(memory_long):
        for j in range(memory_wide):
            print(memory[i][j],end=' ')
        print()
    print("\nOutput:")
    i = 0
    for idx,char in enumerate(print_list):
        i += 1
        if char == '\n':
            i = 0
            print()
        else:
            print(char, end=' ' if i % 12 != 0 else '\n')
    print('\r', end='')

file = None
wait_sec = 0.1
memory_wide = 12
memory_long = 10
is_en = False

if "--speed" in sys.argv:
    try:
        wait_sec = float(sys.argv[sys.argv.index("--speed") + 1])
    except:
        wait_sec = 0.1
if "--f" in sys.argv:
    file = sys.argv[sys.argv.index("--f") + 1]
    try:
        file_end_text = file[-2:]
        if file_end_text != 'bf' and file_end_text != 'Bf' and file_end_text != 'bF' and file_end_text != 'BF':
            file = None
    except:
        file = None
if "--mem" in sys.argv:
    try:
        memory_long,memory_wide = sys.argv[sys.argv.index("--mem") + 1].split('x')
        memory_long = int(memory_long)
        memory_wide = int(memory_wide)
    except:
        memory_wide = 12
        memory_long = 10
if "--en" in sys.argv:
    is_en = True

root = tk.Tk()
root.withdraw()

filetype = [("Brainfuck files", "*.bf")]
if file is None:
    if is_en:
        file = filedialog.askopenfilename(title="Please select a Brainfuck program file", initialdir="/", filetypes=filetype)
    else:
        file = filedialog.askopenfilename(title="请选择Brainfuck程序文件", initialdir="/", filetypes=filetype)

    if not file:
        if is_en:
            print("Cancelled")
        else:
            print("已取消")
        exit()

try:
    with open(file, 'r') as f:
        text = f.read()
except:
    input("Error:File not found")# 未找到文件
    exit()

prl = []
memory = [[0]*memory_wide for _ in range(memory_long)]
pointer = [0,0]

bracket_map = {}
stack = []
for i, char in enumerate(text):
    if char == '[': stack.append(i)
    elif char == ']':
        if not stack:
            input("Error:Extra bracket")# 多余的方括号
            exit()
        start = stack.pop()
        bracket_map[start] = i
        bracket_map[i] = start
if stack:
    input("Error:Unclosed bracket")# 未闭合的方括号
    exit()

i = 0
is_run = False
try:
    while i < len(text):
        char = text[i]
        if char == '>':
            pointer[1] = (pointer[1]+1) % memory_wide
            if pointer[1] == 0: pointer[0] = (pointer[0]+1) % memory_long
        elif char == '<':
            pointer[1] = (pointer[1]-1) % memory_wide
            if pointer[1] == memory_wide-1: pointer[0] = (pointer[0]-1) % memory_long
        elif char == '+':
            memory[pointer[0]][pointer[1]] = (memory[pointer[0]][pointer[1]] +1) % 256
        elif char == '-':
            memory[pointer[0]][pointer[1]] = (memory[pointer[0]][pointer[1]] -1)
            if memory[pointer[0]][pointer[1]] > 255 or memory[pointer[0]][pointer[1]] < 0:
                memory[pointer[0]][pointer[1]] = 0
        elif char == '.':
            prl.append(chr(memory[pointer[0]][pointer[1]]))
        elif char == ',':
            if is_run:
                print()
            if is_en:
                c = input("请输入一个字符:")
            else:
                c = input("请输入一个字符:")
            if not c is None and c != '':
                memory[pointer[0]][pointer[1]] = ord(c[0])
                code = ord(c[0])
                if code < 256:
                    memory[pointer[0]][pointer[1]] = code
        elif char == '[' and not memory[pointer[0]][pointer[1]]:
            i = bracket_map[i]
        elif char == ']' and memory[pointer[0]][pointer[1]]:
            i = bracket_map[i]
        i += 1
        is_run = True
        reset_output(prl)
        time.sleep(wait_sec)
except KeyboardInterrupt:
    reset_output(prl)

if is_en:
    input("\nRun ended, press Enter to exit")
else:
    input("\n运行结束,按回车退出")
