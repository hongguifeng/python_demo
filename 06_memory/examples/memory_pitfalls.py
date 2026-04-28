"""
内存陷阱 — C/C++ 开发者常犯的错误
"""

import sys

print("=== 陷阱 1: 可变默认参数 ===")
# 这是最经典的 Python 陷阱

def append_to_bad(item, lst=[]):
    """默认参数在定义时创建一次！"""
    lst.append(item)
    return lst

r1 = append_to_bad(1)
r2 = append_to_bad(2)
r3 = append_to_bad(3)
print(f"bad: r1={r1}, r2={r2}, r3={r3}")  # 全是 [1, 2, 3]！

def append_to_good(item, lst=None):
    """正确做法"""
    if lst is None:
        lst = []
    lst.append(item)
    return lst

r1 = append_to_good(1)
r2 = append_to_good(2)
print(f"good: r1={r1}, r2={r2}")

print("\n=== 陷阱 2: 列表乘法创建引用 ===")
# C: int matrix[3][3] = {0};  — 独立的内存
# Python:
matrix_bad = [[0] * 3] * 3  # 3 行都指向同一个列表！
matrix_bad[0][0] = 1
print(f"bad matrix:  {matrix_bad}")  # 三行都被修改了！

matrix_good = [[0] * 3 for _ in range(3)]
matrix_good[0][0] = 1
print(f"good matrix: {matrix_good}")

print("\n=== 陷阱 3: += 对可变和不可变对象的行为不同 ===")

# 不可变对象：创建新对象
a = 10
b = a
a += 1
print(f"int: a={a}, b={b} (b 不变)")

# 可变对象：原地修改！
a = [1, 2]
b = a
a += [3]  # 等价于 a.extend([3])，不是 a = a + [3]
print(f"list +=: a={a}, b={b} (b 也变了！)")

# 但 + 会创建新对象
a = [1, 2]
b = a
a = a + [3]  # 创建新列表
print(f"list + : a={a}, b={b} (b 不变)")

print("\n=== 陷阱 4: tuple 中的可变元素 ===")
t = ([1, 2], [3, 4])
# t[0] = [5, 6]  # TypeError! tuple 不可变
t[0].append(3)    # 但 tuple 中的 list 可以修改！
print(f"tuple with mutable: {t}")

# 更诡异的情况
t = ([1, 2],)
try:
    t[0] += [3, 4]  # TypeError! 但列表已经被修改了！
except TypeError:
    print(f"t[0] += [3,4]: TypeError 但 t = {t}")

print("\n=== 陷阱 5: 大对象的内存 ===")

# 字符串拼接 — 每次 + 创建新对象 O(n²)
# C: 预分配缓冲区后 strcat
# Python: 用 join

# 差（O(n²)）
def concat_bad(n):
    s = ""
    for i in range(n):
        s += str(i) + ","
    return s

# 好（O(n)）
def concat_good(n):
    return ",".join(str(i) for i in range(n))

import time
n = 50000
t1 = time.perf_counter()
concat_bad(n)
t2 = time.perf_counter()
concat_good(n)
t3 = time.perf_counter()
print(f"\n字符串拼接 ({n} 次):")
print(f"  += 方式: {t2-t1:.4f}s")
print(f"  join:    {t3-t2:.4f}s")
print(f"  加速比:  {(t2-t1)/(t3-t2):.1f}x")

print("\n=== 内存优化技巧 ===")

# 1. 使用 __slots__ 减少内存
class PointDict:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class PointSlots:
    __slots__ = ('x', 'y')
    def __init__(self, x, y):
        self.x = x
        self.y = y

p1 = PointDict(1, 2)
p2 = PointSlots(1, 2)
print(f"普通类实例: {sys.getsizeof(p1)} + {sys.getsizeof(p1.__dict__)} bytes")
print(f"__slots__: {sys.getsizeof(p2)} bytes")

# 2. 使用 array 模块存储同类型数据
import array
lst = list(range(1000))
arr = array.array('i', range(1000))  # 'i' = signed int
print(f"\n1000 个 int:")
print(f"  list:  {sys.getsizeof(lst):,} bytes")
print(f"  array: {sys.getsizeof(arr):,} bytes")

# 3. 使用生成器而非列表处理大数据
# sum([x**2 for x in range(1000000)])  # 创建百万元素列表
# sum(x**2 for x in range(1000000))    # 生成器，几乎不占内存
