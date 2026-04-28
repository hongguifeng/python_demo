"""
Python 性能优化技巧

面向 C/C++ 开发者的优化指南。
"""

import time
import sys
from functools import lru_cache

def benchmark(name, func, *args, runs=3):
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = func(*args)
        times.append(time.perf_counter() - start)
    avg = sum(times) / len(times)
    print(f"  {name:30s} {avg*1000:>10.2f}ms")
    return result

N = 500_000

print("=== 技巧 1: 使用内置函数（C 实现）===")
# Python 内置函数是 C 实现的，比纯 Python 循环快得多

def sum_python(n):
    total = 0
    for i in range(n):
        total += i
    return total

def sum_builtin(n):
    return sum(range(n))

benchmark("Python 循环 sum", sum_python, N)
benchmark("内置 sum(range())", sum_builtin, N)

print("\n=== 技巧 2: 列表推导式 vs 循环 ===")

def squares_loop(n):
    result = []
    for i in range(n):
        result.append(i ** 2)
    return result

def squares_comprehension(n):
    return [i ** 2 for i in range(n)]

def squares_map(n):
    return list(map(lambda x: x ** 2, range(n)))

benchmark("for 循环 + append", squares_loop, N)
benchmark("列表推导式", squares_comprehension, N)
benchmark("map(lambda)", squares_map, N)

print("\n=== 技巧 3: 字符串拼接 ===")

def concat_plus(n):
    s = ""
    for i in range(n):
        s += str(i)
    return len(s)

def concat_join(n):
    return len("".join(str(i) for i in range(n)))

def concat_join_list(n):
    return len("".join([str(i) for i in range(n)]))

n = 50000
benchmark("字符串 +=", concat_plus, n)
benchmark("join(生成器)", concat_join, n)
benchmark("join(列表)", concat_join_list, n)

print("\n=== 技巧 4: 查找性能 ===")

data = list(range(100000))
data_set = set(data)

def search_list():
    return sum(1 for x in range(0, 100000, 100) if x in data)

def search_set():
    return sum(1 for x in range(0, 100000, 100) if x in data_set)

benchmark("list 中查找 (O(n))", search_list)
benchmark("set 中查找 (O(1))", search_set)

print("\n=== 技巧 5: 局部变量 vs 全局变量 ===")
# CPython 中局部变量访问比全局变量快（LOAD_FAST vs LOAD_GLOBAL）

global_data = list(range(1000))

def access_global():
    total = 0
    for _ in range(1000):
        for x in global_data:
            total += x
    return total

def access_local():
    local_data = list(range(1000))
    total = 0
    for _ in range(1000):
        for x in local_data:
            total += x
    return total

benchmark("全局变量访问", access_global)
benchmark("局部变量访问", access_local)

print("\n=== 技巧 6: 缓存 ===")

def fib_naive(n):
    if n < 2:
        return n
    return fib_naive(n-1) + fib_naive(n-2)

@lru_cache(maxsize=None)
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n-1) + fib_cached(n-2)

benchmark("fibonacci(30) 无缓存", fib_naive, 30, runs=1)
benchmark("fibonacci(30) lru_cache", fib_cached, 30, runs=1)

print("\n=== 技巧 7: 选择合适的数据结构 ===")
from collections import deque

def list_insert_left(n):
    lst = []
    for i in range(n):
        lst.insert(0, i)

def deque_append_left(n):
    dq = deque()
    for i in range(n):
        dq.appendleft(i)

n = 50000
benchmark("list.insert(0, x) O(n²)", list_insert_left, n)
benchmark("deque.appendleft(x) O(n)", deque_append_left, n)

print("\n=== 技巧 8: __slots__ 节省内存和加速 ===")

class PointNormal:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

def create_normal(n):
    return [PointNormal(i, i) for i in range(n)]

def create_slots(n):
    return [PointSlots(i, i) for i in range(n)]

n = 100000
benchmark("普通类创建实例", create_normal, n)
benchmark("__slots__ 创建实例", create_slots, n)

print("\n=== 优化决策树 ===")
print("""
性能不够?
│
├── 算法复杂度有问题? → 换更好的算法 (最大收益!)
│
├── Python 循环太慢? → 用内置函数/推导式/NumPy
│
├── I/O 是瓶颈? → asyncio / 多线程
│
├── CPU 是瓶颈?
│   ├── 可以并行? → multiprocessing / ProcessPoolExecutor
│   └── 热点代码? → C 扩展 / Cython / pybind11
│
├── 内存不够?
│   ├── 大数据? → 生成器 / 流式处理
│   └── 对象太多? → __slots__ / array / numpy
│
└── 以上都不行? → 考虑其他语言 (Rust/Go/C++)
                   或者 PyPy (JIT 编译的 Python)
""".strip())
