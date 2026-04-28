"""
字节码演示 —— Python 的 "目标文件"

C/C++ 开发者类比：
  gcc -S main.c  →  查看汇编
  dis.dis(func)  →  查看 Python 字节码
"""

import dis
import sys

# 定义一个简单函数
def add(a, b):
    return a + b

# 查看字节码（类似 objdump -d）
print("=== add(a, b) 的字节码 ===")
dis.dis(add)

print("\n=== 更复杂的例子 ===")
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

dis.dis(factorial)

# 查看代码对象的属性（类似 ELF section headers）
print("\n=== 代码对象属性 ===")
code = factorial.__code__
print(f"  函数名:     {code.co_name}")
print(f"  参数数量:   {code.co_argcount}")
print(f"  局部变量:   {code.co_varnames}")
print(f"  常量:       {code.co_consts}")
print(f"  字节码大小: {len(code.co_code)} bytes")
print(f"  源文件:     {code.co_filename}")
print(f"  起始行号:   {code.co_firstlineno}")

# 验证函数正确性
print(f"\n=== 验证 ===")
print(f"  add(3, 4)      = {add(3, 4)}")
print(f"  factorial(10)  = {factorial(10)}")
print(f"  factorial(20)  = {factorial(20)}")  # Python 大整数，不会溢出！
