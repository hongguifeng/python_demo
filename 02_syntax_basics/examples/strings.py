"""
Python 字符串 —— 不可变的 Unicode 对象

C: char* 是字节数组，需要手动管理
C++: std::string 可变，但不是原生 Unicode
Python: str 是不可变的 Unicode 序列
"""

print("=== 字符串是不可变的 ===")
s = "hello"
# s[0] = 'H'  # TypeError! 不像 C 的 char[]
s2 = 'H' + s[1:]  # 创建新字符串
print(f"原始: {s}, 新的: {s2}")

print("\n=== 字符串字面量 ===")
single = 'hello'
double = "hello"
triple = """多行
字符串"""
raw = r"不转义 \n \t"  # 类似 C++ 的 R"(...)"
f_string = f"1 + 1 = {1 + 1}"  # 格式化字符串（C 的 sprintf 的优雅替代）

print(f"单引号: {single}")
print(f"双引号: {double}")
print(f"三引号: {triple!r}")
print(f"原始串: {raw}")
print(f"f-string: {f_string}")

print("\n=== f-string 格式化（对比 printf/sprintf）===")
name = "Alice"
age = 30
pi = 3.14159265

# C: printf("Name: %-10s Age: %03d Pi: %.2f\n", name, age, pi);
# Python:
print(f"Name: {name:<10s} Age: {age:03d} Pi: {pi:.2f}")

# 支持任意表达式
print(f"2^10 = {2**10}")
print(f"大写: {'hello'.upper()}")

# 调试格式（Python 3.8+）
x = 42
print(f"{x = }")        # 输出: x = 42
print(f"{x * 2 = }")    # 输出: x * 2 = 84

print("\n=== 常用字符串方法（C 中需要 <string.h>）===")
s = "  Hello, World!  "
print(f"strip():    {s.strip()!r}")
print(f"split(','):  {'a,b,c'.split(',')}")
print(f"join():     {','.join(['a', 'b', 'c'])}")
print(f"replace():  {'hello'.replace('l', 'L')}")
print(f"startswith: {'hello'.startswith('he')}")
print(f"find():     {'hello world'.find('world')}")  # 类似 strstr
print(f"count():    {'banana'.count('a')}")
print(f"isdigit():  {'123'.isdigit()}")

print("\n=== 字符串与字节串（C 开发者必知）===")
# Python3 严格区分 str（文本）和 bytes（字节）
text = "你好世界"                    # str: Unicode 字符
data = text.encode('utf-8')         # bytes: 字节序列
back = data.decode('utf-8')         # 解码回 str

print(f"str:   {text!r} (len={len(text)})")
print(f"bytes: {data!r} (len={len(data)})")
print(f"back:  {back!r}")

# 这个区分很重要：网络 I/O、文件 I/O 处理的是 bytes
# 文本处理用 str。C 中这两个概念是混在一起的。

print("\n=== 字符串是序列 ===")
s = "Python"
print(f"索引:  s[0]={s[0]!r}, s[-1]={s[-1]!r}")
print(f"切片:  s[1:4]={s[1:4]!r}")
print(f"反转:  s[::-1]={s[::-1]!r}")
print(f"遍历:  {[c for c in s]}")
print(f"成员:  {'th' in s} = {'th' in s}")
