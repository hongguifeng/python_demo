"""
推导式 (Comprehensions) — Python 最强大的语法糖之一

C/C++ 没有等价物（C++20 ranges 有点接近但远不如简洁）。

语法骨架：

    [expr for item in iterable if condition]
    {expr for item in iterable if condition}
    {key: value for item in iterable if condition}
    (expr for item in iterable if condition)

阅读顺序：
1. 先看结果表达式 `expr`
2. 再看数据来源 `for item in iterable`
3. 最后看过滤条件 `if condition`

如果有多个 `for`，就按从左到右展开成嵌套循环。
"""

print("=== 列表推导式 (List Comprehension) ===")

# 基本形式：
# [表达式 for 变量 in 可迭代对象 if 条件]

# C 风格：
# int squares[10];
# for (int i = 0; i < 10; i++) squares[i] = i * i;

# Python 推导式：
squares = [x**2 for x in range(10)]
print(f"平方: {squares}")

# 带条件
evens = [x for x in range(20) if x % 2 == 0]
print(f"偶数: {evens}")

# 等价的普通循环
evens_loop = []
for x in range(20):
    if x % 2 == 0:
        evens_loop.append(x)
assert evens == evens_loop

# 嵌套循环
# 顺序和普通循环一致：先 for x，再 for y，最后 if
pairs = [(x, y) for x in range(3) for y in range(3) if x != y]
print(f"不相等的配对: {pairs}")

# 实际应用：矩阵转置
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"\n原矩阵:  {matrix}")
print(f"转置后:  {transposed}")

# 扁平化嵌套列表
flat = [x for row in matrix for x in row]
print(f"扁平化: {flat}")

print("\n=== 字典推导式 ===")
# 形式：{key_expr: value_expr for item in iterable if condition}
# 快速创建映射
ascii_map = {chr(i): i for i in range(ord('a'), ord('g'))}
print(f"ASCII 映射: {ascii_map}")

# 反转字典
inverted = {v: k for k, v in ascii_map.items()}
print(f"反转:       {inverted}")

# 过滤字典
scores = {"Alice": 95, "Bob": 60, "Charlie": 85, "David": 45}
passed = {k: v for k, v in scores.items() if v >= 60}
print(f"及格的: {passed}")

print("\n=== 集合推导式 ===")
# 形式：{expr for item in iterable if condition}
# 获取所有唯一的首字母
words = ["apple", "banana", "avocado", "cherry", "blueberry"]
initials = {w[0] for w in words}
print(f"首字母: {initials}")

print("\n=== 生成器表达式（延迟计算）===")
# 形式：(expr for item in iterable if condition)
# 列表推导式 → 立即生成全部
# 生成器表达式 → 按需生成（节省内存）

# 这会立即创建一个包含 100 万个元素的列表
# big_list = [x**2 for x in range(1_000_000)]

# 这只创建一个生成器对象，不占内存
big_gen = (x**2 for x in range(1_000_000))
print(f"生成器: {big_gen}")
print(f"类型:   {type(big_gen).__name__}")

# 可以直接传给函数
total = sum(x**2 for x in range(1_000_000))
print(f"1到999999的平方和: {total}")

# 内存对比
import sys
list_mem = sys.getsizeof([x for x in range(10000)])
gen_mem = sys.getsizeof(x for x in range(10000))
print(f"\n10000 个元素:")
print(f"  list 占用: {list_mem:,} bytes")
print(f"  generator: {gen_mem:,} bytes (恒定大小!)")

print("\n=== 推导式中的赋值表达式 (Python 3.8+) ===")
# 在推导式中使用海象运算符避免重复计算
import math
data = [2, 5, 8, 15, 20, 25, 30]
results = [(x, y) for x in data if (y := math.sqrt(x)) > 3]
print(f"sqrt > 3 的: {results}")
