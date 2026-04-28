"""
动态类型演示

C++ 中类型是编译期确定的，Python 中类型是运行时的。
"""

print("=== 变量可以绑定到任意类型 ===")
x = 42
print(f"x = {x!r:20s}  type = {type(x).__name__}")

x = 3.14
print(f"x = {x!r:20s}  type = {type(x).__name__}")

x = "hello"
print(f"x = {x!r:20s}  type = {type(x).__name__}")

x = [1, 2, 3]
print(f"x = {x!r:20s}  type = {type(x).__name__}")

x = {"key": "value"}
print(f"x = {x!r:20s}  type = {type(x).__name__}")

x = lambda n: n * 2  # 函数也是对象！
print(f"x = {x!r:20s}  type = {type(x).__name__}")
print(f"x(21) = {x(21)}")

# isinstance() — 运行时类型检查（类似 dynamic_cast）
print("\n=== isinstance() — 运行时类型检查 ===")
def describe(obj):
    """类似 C++ 的函数重载，但在运行时分发"""
    if isinstance(obj, int):
        print(f"  {obj} 是整数, 二进制: {bin(obj)}")
    elif isinstance(obj, float):
        print(f"  {obj} 是浮点数, 科学计数法: {obj:.2e}")
    elif isinstance(obj, str):
        print(f"  {obj!r} 是字符串, 长度: {len(obj)}")
    elif isinstance(obj, (list, tuple)):
        print(f"  {obj} 是序列, 长度: {len(obj)}")
    else:
        print(f"  {obj} 是 {type(obj).__name__}")

describe(42)
describe(3.14)
describe("hello")
describe([1, 2, 3])
describe((1, 2))

# 类型不匹配是运行时错误，不是编译时错误
print("\n=== 类型错误是运行时的 ===")
def add_one(x):
    return x + 1

print(f"add_one(41) = {add_one(41)}")
try:
    add_one("hello")  # C++ 编译期就会报错，Python 运行时才报错
except TypeError as e:
    print(f"add_one('hello') → TypeError: {e}")
