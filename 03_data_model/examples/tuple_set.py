"""
tuple 和 set

tuple: 不可变序列（类似 const std::vector 或 std::tuple）
set: 无序不重复集合（类似 std::unordered_set）
"""

print("=== tuple — 不可变序列 ===")
# 创建
point = (3, 4)
rgb = (255, 128, 0)
single = (42,)      # 单元素 tuple 需要逗号！
not_tuple = (42)     # 这只是 int 42
empty = ()

print(f"point = {point}, type = {type(point).__name__}")
print(f"single = {single}, type = {type(single).__name__}")
print(f"not_tuple = {not_tuple}, type = {type(not_tuple).__name__}")

# tuple 可以用作 dict 的 key（因为不可变，可以 hash）
locations = {(0, 0): "origin", (1, 0): "east", (0, 1): "north"}
print(f"\ntuple 作为 dict key: locations[(0,0)] = {locations[(0, 0)]}")

# list 不能作为 key
try:
    d = {[1, 2]: "test"}
except TypeError as e:
    print(f"list 作为 key: TypeError: {e}")

# namedtuple — 给 tuple 加上字段名（类似 C 的 struct）
print("\n=== namedtuple — 轻量 struct ===")
from collections import namedtuple

# 类似: struct Point { double x; double y; };
Point = namedtuple('Point', ['x', 'y'])
p = Point(3.0, 4.0)
print(f"p = {p}")
print(f"p.x = {p.x}, p.y = {p.y}")
print(f"p[0] = {p[0]}")  # 也支持索引
print(f"距离 = {(p.x**2 + p.y**2)**0.5:.2f}")

# 可以用 _replace 创建修改后的新 tuple
p2 = p._replace(x=5.0)
print(f"p2 = {p2}")

print("\n" + "=" * 40)
print("=== set — 无序不重复集合 ===")

# 创建
s1 = {1, 2, 3, 4, 5}
s2 = {4, 5, 6, 7, 8}
empty_set = set()  # 注意：{} 是空 dict，不是空 set！

print(f"s1 = {s1}")
print(f"s2 = {s2}")

# 集合运算（C++ 的 std::set_union 等，但语法更简洁）
print(f"\n交集 s1 & s2:       {s1 & s2}")
print(f"并集 s1 | s2:       {s1 | s2}")
print(f"差集 s1 - s2:       {s1 - s2}")
print(f"对称差集 s1 ^ s2:   {s1 ^ s2}")
print(f"子集 {{1,2}} <= s1:  {{1,2}} <= s1 = {({1,2} <= s1)}")

# 常见用法：去重
lst = [1, 2, 2, 3, 3, 3, 4, 4, 4, 4]
unique = list(set(lst))  # 注意：不保持顺序
print(f"\n去重: {lst} → {sorted(set(lst))}")

# 保持顺序的去重
seen = set()
ordered_unique = []
for x in lst:
    if x not in seen:
        seen.add(x)
        ordered_unique.append(x)
print(f"保序去重: {ordered_unique}")

# Python 3.7+ 更简洁的保序去重
ordered_unique2 = list(dict.fromkeys(lst))
print(f"dict.fromkeys 去重: {ordered_unique2}")

# 成员测试 O(1)（比 list 的 O(n) 快得多）
print(f"\n3 in s1: {3 in s1}")  # O(1)

# frozenset — 不可变 set（可以作为 dict key 或 set 元素）
print("\n=== frozenset ===")
fs = frozenset([1, 2, 3])
print(f"frozenset: {fs}")
# fs.add(4)  # AttributeError! 不可变

# set of sets 需要 frozenset
power_set_example = {frozenset(), frozenset([1]), frozenset([2]), frozenset([1, 2])}
print(f"set of frozensets: {power_set_example}")
