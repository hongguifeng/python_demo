"""
dict 深入 —— Python 最重要的数据结构

底层是哈希表（类似 C++ 的 std::unordered_map）。
Python 3.7+ dict 保持插入顺序（类似 C++ 的 LinkedHashMap）。
"""

print("=== 创建 dict ===")
# 类似 C 的 struct，但完全动态
person = {"name": "Alice", "age": 30, "city": "Beijing"}
print(f"person = {person}")

# 另一种创建方式
config = dict(host="localhost", port=8080, debug=True)
print(f"config = {config}")

# 从键值对列表创建
pairs = [("a", 1), ("b", 2), ("c", 3)]
d = dict(pairs)
print(f"dict(pairs) = {d}")

print("\n=== 基本操作 ===")
d = {"x": 1, "y": 2, "z": 3}

# 访问（O(1) 平均）
print(f"d['x'] = {d['x']}")

# 访问不存在的键
# d['w']  # KeyError! 类似 C++ 的 map::at()
print(f"d.get('w') = {d.get('w')}")          # 返回 None
print(f"d.get('w', 0) = {d.get('w', 0)}")    # 返回默认值

# 设置
d['w'] = 4
print(f"设置 d['w']=4: {d}")

# 删除
del d['w']
print(f"del d['w']: {d}")

# pop（删除并返回）
val = d.pop('z')
print(f"d.pop('z') = {val}, d = {d}")

print("\n=== 遍历 ===")
scores = {"Alice": 95, "Bob": 87, "Charlie": 92}

print("遍历键:")
for key in scores:  # 默认遍历键
    print(f"  {key}")

print("遍历键值对:")
for key, value in scores.items():
    print(f"  {key}: {value}")

print("遍历值:")
for value in scores.values():
    print(f"  {value}")

print("\n=== dict 的高级用法 ===")

# setdefault — 不存在则设置
word_count = {}
words = "hello world hello python world hello".split()
for word in words:
    word_count.setdefault(word, 0)
    word_count[word] += 1
print(f"词频统计: {word_count}")

# collections.Counter — 更优雅的词频统计
from collections import Counter
word_count2 = Counter(words)
print(f"Counter:  {dict(word_count2)}")
print(f"最常见:   {word_count2.most_common(2)}")

# collections.defaultdict — 自动初始化
from collections import defaultdict
# 类似 C++ 的 map 默认构造
graph = defaultdict(list)  # 值默认为空列表
edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A")]
for src, dst in edges:
    graph[src].append(dst)
print(f"\n邻接表: {dict(graph)}")

print("\n=== dict 合并 ===")
# Python 3.9+
d1 = {"a": 1, "b": 2}
d2 = {"b": 3, "c": 4}
merged = d1 | d2  # 类似 {**d1, **d2}
print(f"d1 | d2 = {merged}")

# 原地合并
d1 |= d2
print(f"d1 |= d2: d1 = {d1}")

print("\n=== dict 推导式 ===")
# 类似列表推导式
squares = {x: x**2 for x in range(6)}
print(f"平方表: {squares}")

# 反转 dict
inverted = {v: k for k, v in squares.items()}
print(f"反转:   {inverted}")

print("\n=== 为什么 dict 如此重要 ===")
# 1. Python 的类实例属性存储在 __dict__ 中
# 2. 模块的全局变量是 dict
# 3. 函数的关键字参数是 dict
# 4. JSON 解析结果是 dict
# 正如 Guido 说的："dict is the backbone of Python"

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(1, 2)
print(f"\n对象的 __dict__: {p.__dict__}")
print(f"模块的 __dict__ 包含: {list(k for k in globals().keys() if not k.startswith('_'))[:8]}...")
