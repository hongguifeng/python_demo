"""
functools 模块 — 函数式编程工具箱
"""

import functools
import time

print("=== functools.lru_cache — 自动缓存 ===")

@functools.lru_cache(maxsize=128)
def fibonacci(n):
    """带自动缓存的递归 — 不用手动实现记忆化"""
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

start = time.perf_counter()
result = fibonacci(100)
elapsed = time.perf_counter() - start
print(f"fib(100) = {result}")
print(f"耗时: {elapsed:.6f}s")
print(f"缓存统计: {fibonacci.cache_info()}")

# Python 3.9+: cache 是不限大小的 lru_cache
@functools.cache
def factorial(n):
    return 1 if n <= 1 else n * factorial(n - 1)

print(f"\n100! = {factorial(100)}")

print("\n=== functools.partial — 偏函数 ===")
# 固定部分参数，创建新函数（类似 C++ 的 std::bind）

def power(base, exponent):
    return base ** exponent

square = functools.partial(power, exponent=2)
cube = functools.partial(power, exponent=3)

print(f"square(5) = {square(5)}")
print(f"cube(5)   = {cube(5)}")

# 实际应用：创建预配置的函数
import json
pretty_json = functools.partial(json.dumps, indent=2, ensure_ascii=False)
data = {"name": "张三", "scores": [90, 85, 92]}
print(f"\n{pretty_json(data)}")

print("\n=== functools.reduce ===")
# 类似 C++ 的 std::accumulate

nums = [1, 2, 3, 4, 5]

# 求和
total = functools.reduce(lambda acc, x: acc + x, nums)
print(f"sum: {total}")

# 求最大值
maximum = functools.reduce(lambda a, b: a if a > b else b, nums)
print(f"max: {maximum}")

# 管道操作
def pipe(*functions):
    """函数组合：pipe(f, g, h)(x) = h(g(f(x)))"""
    def pipeline(value):
        return functools.reduce(lambda v, f: f(v), functions, value)
    return pipeline

process = pipe(
    lambda x: x * 2,
    lambda x: x + 10,
    lambda x: f"result: {x}"
)
print(f"pipe(5) = {process(5)}")

print("\n=== functools.total_ordering ===")
# 只需要定义 __eq__ 和一个比较方法，自动生成其余

@functools.total_ordering
class Version:
    def __init__(self, major, minor, patch):
        self.major = major
        self.minor = minor
        self.patch = patch

    def __eq__(self, other):
        return (self.major, self.minor, self.patch) == \
               (other.major, other.minor, other.patch)

    def __lt__(self, other):
        return (self.major, self.minor, self.patch) < \
               (other.major, other.minor, other.patch)

    def __repr__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

versions = [Version(2, 0, 0), Version(1, 9, 1), Version(1, 10, 0)]
versions.sort()
print(f"排序: {versions}")
print(f"v1.9.1 <= v1.10.0: {Version(1, 9, 1) <= Version(1, 10, 0)}")

print("\n=== functools.singledispatch — 单分派泛型函数 ===")
# 类似 C++ 的函数重载，但基于运行时类型

@functools.singledispatch
def format_value(value):
    return str(value)

@format_value.register(int)
def _(value):
    return f"整数: {value:,}"

@format_value.register(float)
def _(value):
    return f"浮点: {value:.4f}"

@format_value.register(list)
def _(value):
    return f"列表[{len(value)}]: {value}"

print(f"format(42):      {format_value(42)}")
print(f"format(3.14):    {format_value(3.14)}")
print(f"format([1,2,3]): {format_value([1, 2, 3])}")
print(f"format('hello'): {format_value('hello')}")
