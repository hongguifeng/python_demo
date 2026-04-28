"""
REPL 功能演示 —— 展示 Python 交互式探索能力

C/C++ 开发者注意：Python 的 dir()/help()/type() 相当于
在运行时拥有了一个内建的 "反射 + 文档查看器"。
"""

# dir() — 查看对象的所有属性和方法
print("=== dir() 示例 ===")
my_list = [1, 2, 3]
# 过滤掉 dunder 方法，只看 "公开" 方法
public_methods = [m for m in dir(my_list) if not m.startswith('_')]
print(f"list 的公开方法: {public_methods}")

# type() — 运行时类型检查（C++ 中类似 typeid）
print("\n=== type() 示例 ===")
values = [42, 3.14, "hello", [1, 2], (1, 2), {1, 2}, {"a": 1}]
for v in values:
    print(f"  {str(v):20s} -> {type(v).__name__}")

# help() 的替代：__doc__ 属性
print("\n=== __doc__ 示例 ===")
print(f"list.append 的文档:\n  {list.append.__doc__}")

# id() — 对象的内存地址（类似 C 的 &variable）
print("\n=== id() 示例（类似取地址 &） ===")
a = [1, 2, 3]
b = a           # b 是 a 的引用（类似 C++ 的引用或指针赋值）
c = a.copy()    # c 是深拷贝
print(f"id(a) = {id(a):#x}")
print(f"id(b) = {id(b):#x}  (与 a 相同 — 同一个对象)")
print(f"id(c) = {id(c):#x}  (与 a 不同 — 不同对象)")
print(f"a is b: {a is b}")   # is 比较的是 id，不是值
print(f"a is c: {a is c}")
print(f"a == c: {a == c}")   # == 比较的是值

# sys 模块 — 类似 C 的运行时信息
print("\n=== sys 模块信息 ===")
import sys
print(f"Python 版本: {sys.version}")
print(f"平台: {sys.platform}")
print(f"整数最大位数: 无限制 (Python 原生支持大整数)")
print(f"  2^100 = {2**100}")
print(f"  在 C 中这需要 GMP 库!")
