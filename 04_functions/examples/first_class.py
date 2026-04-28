"""
函数作为一等公民 (First-class Functions)

C 中函数不是值（需要函数指针）。
Python 中函数就是对象，可以赋值、传递、存储。
"""

print("=== 函数是对象 ===")

def greet(name):
    return f"Hello, {name}!"

# 函数有属性
print(f"函数名: {greet.__name__}")
print(f"函数类型: {type(greet)}")
print(f"函数 id: {id(greet):#x}")

# 赋值给变量（类似函数指针赋值，但更自然）
say_hi = greet
print(f"say_hi('World') = {say_hi('World')}")

print("\n=== 函数作为参数（类似 qsort 的 compare 参数）===")

def apply(func, value):
    """类似 C 接收函数指针的函数"""
    return func(value)

def double(x):
    return x * 2

def square(x):
    return x ** 2

print(f"apply(double, 5) = {apply(double, 5)}")
print(f"apply(square, 5) = {apply(square, 5)}")

# 内置高阶函数
print("\n=== map / filter / reduce ===")
nums = [1, 2, 3, 4, 5]

# map: 类似 std::transform
doubled = list(map(lambda x: x * 2, nums))
print(f"map(x*2): {doubled}")

# filter: 类似 std::copy_if
evens = list(filter(lambda x: x % 2 == 0, nums))
print(f"filter(偶数): {evens}")

# 但 Python 更推荐用推导式：
doubled2 = [x * 2 for x in nums]
evens2 = [x for x in nums if x % 2 == 0]
print(f"推导式更 Pythonic: {doubled2}, {evens2}")

# reduce: 类似 std::accumulate
from functools import reduce
total = reduce(lambda acc, x: acc + x, nums, 0)
print(f"reduce(+): {total}")

print("\n=== 函数作为返回值 ===")

def make_multiplier(factor):
    """返回一个函数（工厂模式）"""
    def multiplier(x):
        return x * factor
    return multiplier

times3 = make_multiplier(3)
times5 = make_multiplier(5)
print(f"times3(4) = {times3(4)}")
print(f"times5(4) = {times5(4)}")
print(f"times3 的类型: {type(times3).__name__}")

print("\n=== 函数存储在数据结构中 ===")
# 类似 C 的函数指针数组，但更灵活
import math

operations = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "^": lambda a, b: a ** b,
}

for op, func in operations.items():
    print(f"  3 {op} 4 = {func(3, 4)}")

print("\n=== lambda 表达式 ===")
# lambda 只能包含单个表达式（不能有语句）
# 类似 C++11 的 [](auto x){ return x*2; }

# 排序中使用（最常见用法）
students = [("Alice", 90), ("Bob", 85), ("Charlie", 92)]
students.sort(key=lambda s: s[1], reverse=True)
print(f"按成绩排序: {students}")

# 立即调用
result = (lambda x, y: x + y)(3, 4)
print(f"立即调用 lambda: {result}")
