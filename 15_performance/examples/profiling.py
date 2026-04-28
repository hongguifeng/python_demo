"""
性能分析工具

类比:
  C/C++: gprof, valgrind --tool=callgrind, perf
  Python: cProfile, timeit, line_profiler
"""

import time
import cProfile
import pstats
from io import StringIO

print("=== timeit — 微基准测试 ===")
# 类似 C 中用 clock_gettime 手动计时

import timeit

# 测试不同的列表创建方式
n = 10000
t1 = timeit.timeit(f"list(range({n}))", number=1000)
t2 = timeit.timeit(f"[i for i in range({n})]", number=1000)
t3 = timeit.timeit(f"[*range({n})]", number=1000)

print(f"list(range()):   {t1:.4f}s")
print(f"[i for i in ...]: {t2:.4f}s")
print(f"[*range()]:      {t3:.4f}s")

# 测试字符串拼接
print("\n字符串操作:")
t1 = timeit.timeit("'+'.join(str(i) for i in range(100))", number=10000)
t2 = timeit.timeit("'+'.join([str(i) for i in range(100)])", number=10000)

print(f"生成器 join: {t1:.4f}s")
print(f"列表 join:   {t2:.4f}s (通常更快，因为 join 需要两次遍历)")

print("\n=== cProfile — 函数级性能分析 ===")
# 类似 gprof

def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def process_data():
    """模拟数据处理流程"""
    data = list(range(10000))

    # 排序
    sorted_data = sorted(data, reverse=True)

    # 过滤
    filtered = [x for x in sorted_data if x % 2 == 0]

    # 映射
    mapped = list(map(lambda x: x ** 2, filtered))

    # 聚合
    total = sum(mapped)
    return total

# 使用 cProfile 分析
print("cProfile 分析 process_data():")
pr = cProfile.Profile()
pr.enable()
result = process_data()
pr.disable()

# 格式化输出
s = StringIO()
ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
ps.print_stats(10)
print(s.getvalue())

print("\n=== time.perf_counter — 手动计时 ===")

def benchmark(func, *args, runs=5):
    """简单的基准测试"""
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        result = func(*args)
        elapsed = time.perf_counter() - start
        times.append(elapsed)
    avg = sum(times) / len(times)
    return avg, result

# 对比不同的查找方式
data_list = list(range(100000))
data_set = set(data_list)
data_dict = {i: True for i in data_list}

target = 99999

avg, _ = benchmark(lambda: target in data_list, runs=100)
print(f"list 查找:   {avg*1000:.4f}ms")

avg, _ = benchmark(lambda: target in data_set, runs=100)
print(f"set 查找:    {avg*1000:.6f}ms")

avg, _ = benchmark(lambda: target in data_dict, runs=100)
print(f"dict 查找:   {avg*1000:.6f}ms")

print("\n=== sys.getsizeof — 内存分析 ===")
import sys

# 对比数据结构的内存开销
structures = {
    "list[1000 int]": list(range(1000)),
    "tuple(1000 int)": tuple(range(1000)),
    "set(1000 int)": set(range(1000)),
    "dict(1000 items)": {i: i for i in range(1000)},
}

print(f"{'结构':25s} {'浅大小':>12s}")
print("-" * 40)
for name, obj in structures.items():
    size = sys.getsizeof(obj)
    print(f"{name:25s} {size:>10,d} B")

print("\n=== 常用分析工具总结 ===")
print("""
内置工具:
  timeit      — 微基准测试（最精确的计时）
  cProfile    — 函数级性能分析
  profile     — 纯 Python 实现（更慢但可扩展）
  tracemalloc — 内存分配追踪

第三方工具:
  line_profiler  — 逐行分析（@profile 装饰器）
    pip install line_profiler
    kernprof -l -v script.py

  memory_profiler — 逐行内存分析
    pip install memory_profiler
    python -m memory_profiler script.py

  py-spy         — 采样分析器（低开销，可附加到运行中的进程）
    pip install py-spy
    py-spy record -o profile.svg -- python script.py

  scalene        — CPU + 内存 + GPU 分析
    pip install scalene
    scalene script.py
""".strip())
