"""
迭代器协议 — Python 的 for 循环工作原理

C++ iterator: begin()/end(), ++, *, !=
Python iterator: __iter__(), __next__(), StopIteration
"""

print("=== for 循环的本质 ===")
# for x in iterable: 等价于：
nums = [1, 2, 3]
iterator = iter(nums)     # 调用 __iter__()
while True:
    try:
        x = next(iterator)  # 调用 __next__()
        print(f"  x = {x}")
    except StopIteration:   # 没有更多元素
        break

print("\n=== 自定义迭代器 ===")

class CountDown:
    """
    C++ 等价需要定义 iterator 类并实现 begin/end/++/*/!=
    Python 只需要两个方法
    """
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self  # 自己就是迭代器

    def __next__(self):
        if self.current <= 0:
            raise StopIteration
        val = self.current
        self.current -= 1
        return val

print("倒计时:")
for n in CountDown(5):
    print(f"  {n}", end="")
print()

# 可以多次使用（但每次需要新建实例）
print(f"list(CountDown(3)) = {list(CountDown(3))}")

print("\n=== 可迭代对象 vs 迭代器 ===")
"""
可迭代对象 (Iterable): 有 __iter__ 方法，返回迭代器
迭代器 (Iterator): 有 __next__ 方法，维护状态

类比：
- 可迭代 = 一本书（可以创建多个书签）
- 迭代器 = 书签（记住当前位置）
"""

class Fibonacci:
    """可迭代对象 — 每次调用 __iter__ 返回新的迭代器"""
    def __init__(self, max_n):
        self.max_n = max_n

    def __iter__(self):
        """每次返回新的迭代器"""
        return FibIterator(self.max_n)

class FibIterator:
    def __init__(self, max_n):
        self.max_n = max_n
        self.a, self.b = 0, 1
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count >= self.max_n:
            raise StopIteration
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        self.count += 1
        return val

fib = Fibonacci(10)
print(f"第一次遍历: {list(fib)}")
print(f"第二次遍历: {list(fib)}")  # 可以重复遍历！

print("\n=== 内置可迭代对象 ===")
# Python 中大量对象都是可迭代的

# range — 不是列表！是惰性的
import sys
r = range(1_000_000)
print(f"range(1M) 内存: {sys.getsizeof(r)} bytes (恒定!)")
print(f"500000 in range(1M): {500000 in r}")  # O(1)!
print(f"range 支持切片: range(10)[2:7] = {list(range(10)[2:7])}")

# 文件是迭代器 — 逐行读取不会全部加载到内存
# with open('big_file.txt') as f:
#     for line in f:       # 一次只在内存中保存一行
#         process(line)

# dict 迭代
d = {"a": 1, "b": 2, "c": 3}
print(f"\ndict keys:   {list(d.keys())}")
print(f"dict values: {list(d.values())}")
print(f"dict items:  {list(d.items())}")

# enumerate 和 zip 也是惰性迭代器
print(f"\nenumerate: {list(enumerate(['a', 'b', 'c']))}")
print(f"zip:       {list(zip([1, 2, 3], ['a', 'b', 'c']))}")
