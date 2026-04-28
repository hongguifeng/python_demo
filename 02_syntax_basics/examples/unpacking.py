"""
多重赋值与解包 (Unpacking)

C++17 有 structured bindings，但 Python 的解包更强大。
"""

print("=== 多重赋值 ===")
# C: int a = 1; int b = 2; int c = 3;
a, b, c = 1, 2, 3
print(f"a={a}, b={b}, c={c}")

# 交换变量 — 不需要临时变量！
# C: int tmp = a; a = b; b = tmp;
a, b = b, a
print(f"交换后: a={a}, b={b}")

print("\n=== 解包序列 ===")
# 解包列表
first, second, third = [10, 20, 30]
print(f"列表解包: {first}, {second}, {third}")

# 解包元组（函数返回多个值的常见模式）
def divmod_custom(a, b):
    """类似 C 通过指针参数返回多个值，Python 直接返回元组"""
    return a // b, a % b

quotient, remainder = divmod_custom(17, 5)
print(f"17 / 5 = {quotient} 余 {remainder}")

print("\n=== 星号解包 (*) — C 没有的特性 ===")
# 收集剩余元素
first, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, rest={rest}")

first, *middle, last = [1, 2, 3, 4, 5]
print(f"first={first}, middle={middle}, last={last}")

*init, last = [1, 2, 3, 4, 5]
print(f"init={init}, last={last}")

print("\n=== 嵌套解包 ===")
# 类似解构嵌套 struct
data = ("Alice", (90, 85, 92))
name, (math, english, science) = data
print(f"学生: {name}, 数学={math}, 英语={english}, 科学={science}")

print("\n=== 在循环中解包 ===")
# 类似 C++ 的 structured bindings in range-for
points = [(1, 2), (3, 4), (5, 6)]
for x, y in points:
    print(f"  点: ({x}, {y}), 距原点: {(x**2 + y**2)**0.5:.2f}")

# 带索引的循环（C 中的 for(int i=0; ...)）
print("\n带索引:")
names = ["Alice", "Bob", "Charlie"]
for i, name in enumerate(names):
    print(f"  [{i}] {name}")

# 同时遍历两个列表（C 中需要用同一个索引）
print("\n同时遍历:")
keys = ["name", "age", "city"]
values = ["Alice", 30, "Beijing"]
for k, v in zip(keys, values):
    print(f"  {k}: {v}")

print("\n=== 字典解包 (**) ===")
defaults = {"color": "red", "size": 10, "weight": 1.0}
overrides = {"size": 20, "name": "widget"}
merged = {**defaults, **overrides}  # 类似 struct 合并
print(f"合并字典: {merged}")
