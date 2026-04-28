"""
itertools — 迭代器工具箱

C++ 的 <algorithm> 头文件的 Python 等价物（惰性版本）。
"""

import itertools

print("=== 无限迭代器 ===")

# count — 无限计数（C 的 for(int i=0; ; i++)）
for i in itertools.islice(itertools.count(10, 3), 5):
    print(f"  count(10, 3): {i}")

# cycle — 无限循环
colors = itertools.cycle(["red", "green", "blue"])
print(f"\ncycle: {[next(colors) for _ in range(7)]}")

# repeat
print(f"repeat(42, 3): {list(itertools.repeat(42, 3))}")

print("\n=== 组合迭代器 ===")

# product — 笛卡尔积（嵌套 for 循环）
print("product('AB', '12'):")
for pair in itertools.product("AB", "12"):
    print(f"  {pair}")

# permutations — 排列
print(f"\npermutations('ABC', 2): {list(itertools.permutations('ABC', 2))}")

# combinations — 组合
print(f"combinations('ABCD', 2): {list(itertools.combinations('ABCD', 2))}")

print("\n=== 过滤和选择 ===")

# takewhile / dropwhile — 类似 C++20 ranges 的 take_while/drop_while
data = [1, 3, 5, 2, 4, 6, 1]
taken = list(itertools.takewhile(lambda x: x < 5, data))
dropped = list(itertools.dropwhile(lambda x: x < 5, data))
print(f"data: {data}")
print(f"takewhile(<5): {taken}")
print(f"dropwhile(<5): {dropped}")

# compress — 用掩码过滤
items = ['a', 'b', 'c', 'd', 'e']
mask = [1, 0, 1, 0, 1]
print(f"\ncompress: {list(itertools.compress(items, mask))}")

# filterfalse — filter 的反面
evens = list(itertools.filterfalse(lambda x: x % 2, range(10)))
print(f"filterfalse(odd): {evens}")

print("\n=== 聚合和分组 ===")

# groupby — 按键分组（类似 SQL 的 GROUP BY）
data = [
    ("A", 1), ("A", 2), ("B", 3), ("B", 4), ("A", 5)
]
# 注意：需要先排序！groupby 只分组连续相同键的元素
data.sort(key=lambda x: x[0])
print("groupby:")
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    items = list(group)
    print(f"  {key}: {items}")

# accumulate — 累积运算（类似 C++ 的 std::partial_sum）
nums = [1, 2, 3, 4, 5]
print(f"\naccumulate(+): {list(itertools.accumulate(nums))}")
print(f"accumulate(*): {list(itertools.accumulate(nums, lambda a, b: a * b))}")

# 运行中的最大值
import operator
data = [3, 1, 4, 1, 5, 9, 2, 6]
running_max = list(itertools.accumulate(data, max))
print(f"running max of {data}: {running_max}")

print("\n=== 连接和展开 ===")

# chain — 连接多个可迭代对象
print(f"chain: {list(itertools.chain([1,2], [3,4], [5,6]))}")

# chain.from_iterable — 展开一层嵌套
nested = [[1, 2], [3, 4], [5, 6]]
print(f"chain.from_iterable: {list(itertools.chain.from_iterable(nested))}")

# zip_longest — 不丢弃较短的
a = [1, 2, 3, 4, 5]
b = ['a', 'b', 'c']
print(f"\nzip:         {list(zip(a, b))}")
print(f"zip_longest: {list(itertools.zip_longest(a, b, fillvalue='-'))}")

print("\n=== 实际应用：高效处理 ===")

# 分批处理（Python 3.12+ 有 itertools.batched）
def batched(iterable, n):
    it = iter(iterable)
    while batch := list(itertools.islice(it, n)):
        yield batch

data = range(17)
print("批处理:")
for batch in batched(data, 5):
    print(f"  {batch}")

# 滑动窗口
def sliding_window(iterable, n):
    it = iter(iterable)
    window = list(itertools.islice(it, n))
    if len(window) == n:
        yield tuple(window)
    for x in it:
        window = window[1:] + [x]
        yield tuple(window)

data = [1, 2, 3, 4, 5, 6]
print(f"\n滑动窗口(3) of {data}:")
for w in sliding_window(data, 3):
    print(f"  {w} → sum={sum(w)}")
