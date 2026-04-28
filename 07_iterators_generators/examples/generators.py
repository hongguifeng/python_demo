"""
生成器 (Generator) — Python 最强大的特性之一

生成器 = 用 yield 简化的迭代器
函数遇到 yield 时暂停执行，下次 next() 从暂停处继续。
C/C++ 没有等价物（C++20 的 coroutine 有点像但复杂得多）。
"""

print("=== 基本生成器 ===")

def countdown(n):
    """生成器函数 — 不是普通函数"""
    print(f"  [开始倒计时 from {n}]")
    while n > 0:
        yield n  # 暂停并返回值
        n -= 1
    print(f"  [倒计时结束]")

# 调用生成器函数不会执行函数体！只返回生成器对象
gen = countdown(3)
print(f"类型: {type(gen)}")

# next() 驱动执行到下一个 yield
print(f"next: {next(gen)}")
print(f"next: {next(gen)}")
print(f"next: {next(gen)}")
# print(f"next: {next(gen)}")  # StopIteration

# 通常用 for 循环消耗
print("\nfor 循环:")
for n in countdown(3):
    print(f"  {n}")

print("\n=== 生成器实现斐波那契 ===")
# 对比前一章的 Fibonacci 类：代码量减少 80%

def fibonacci():
    """无限斐波那契数列"""
    a, b = 0, 1
    while True:  # 无限序列！
        yield a
        a, b = b, a + b

# 取前 15 个
from itertools import islice
print(f"Fib: {list(islice(fibonacci(), 15))}")

print("\n=== 生成器表达式 ===")
# 列表推导式的 () 版本 — 惰性计算
import sys

list_comp = [x**2 for x in range(10000)]
gen_expr = (x**2 for x in range(10000))

print(f"列表推导式内存: {sys.getsizeof(list_comp):,} bytes")
print(f"生成器表达式:   {sys.getsizeof(gen_expr):,} bytes")

# 直接传给函数
total = sum(x**2 for x in range(1000))
print(f"sum(x² for x in range(1000)) = {total}")

print("\n=== 生成器构建数据管道 ===")
# 类似 Unix 管道: cat file | grep pattern | sort | head

def read_lines(text):
    """模拟文件读取"""
    for line in text.strip().split('\n'):
        yield line

def filter_lines(lines, keyword):
    """过滤包含关键字的行"""
    for line in lines:
        if keyword in line:
            yield line

def uppercase(lines):
    """转大写"""
    for line in lines:
        yield line.upper()

log = """
2024-01-01 INFO: Server started
2024-01-01 ERROR: Connection failed
2024-01-02 INFO: Request processed
2024-01-02 ERROR: Timeout exceeded
2024-01-03 INFO: Shutdown initiated
"""

# 构建管道 — 没有中间列表，全是惰性的！
pipeline = uppercase(filter_lines(read_lines(log), "ERROR"))
print("错误日志:")
for line in pipeline:
    print(f"  {line}")

print("\n=== yield from — 委托生成器 ===")

def chain(*iterables):
    """合并多个可迭代对象（类似 itertools.chain）"""
    for iterable in iterables:
        yield from iterable  # 委托给子迭代器

result = list(chain([1, 2], [3, 4], [5, 6]))
print(f"chain: {result}")

# 用于树遍历
def flatten(nested):
    """递归展开嵌套列表"""
    for item in nested:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

nested = [1, [2, [3, 4]], [5, 6], [[7], 8]]
print(f"flatten: {list(flatten(nested))}")

print("\n=== 生成器的 send() 方法 ===")
# yield 不仅可以产出值，还可以接收值！

def accumulator():
    """累加器 — 接收值并返回累加结果"""
    total = 0
    while True:
        value = yield total  # 产出 total，接收 send 的值
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)  # 启动生成器（运行到第一个 yield）
print(f"send(10): {acc.send(10)}")
print(f"send(20): {acc.send(20)}")
print(f"send(30): {acc.send(30)}")
