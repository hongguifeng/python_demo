"""
垃圾回收 (GC) — 处理循环引用

引用计数无法处理循环引用。
Python 有额外的循环垃圾回收器（标记-清除 + 分代回收）。
"""

import gc
import sys
import weakref

print("=== 循环引用问题 ===")

class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

    def __del__(self):
        print(f"  销毁 {self.name}")

# 创建循环引用
print("创建循环引用:")
a = Node("A")
b = Node("B")
a.other = b
b.other = a

# 删除外部引用
del a
del b
# 此时 A 和 B 互相引用，引用计数不为 0
# 但没有外部引用可以到达它们 — 这就是垃圾！
print("del a, b 后 — 引用计数不为 0，但已无法访问")

# 强制 GC
print("强制 GC:")
gc.collect()

print("\n=== GC 分代回收 ===")
# 基于"弱代假说"：大多数对象生命周期很短
# 第 0 代：新创建的对象
# 第 1 代：经历过一次 GC 的对象
# 第 2 代：经历过多次 GC 的对象

counts = gc.get_count()
thresholds = gc.get_threshold()
print(f"当前各代对象数:   {counts}")
print(f"GC 触发阈值:      {thresholds}")
print(f"GC 启用状态:       {gc.isenabled()}")

stats = gc.get_stats()
for i, s in enumerate(stats):
    print(f"  第{i}代: collections={s['collections']}, collected={s['collected']}")

print("\n=== weakref — 弱引用 ===")
# 类似 C++ 的 weak_ptr
# 不增加引用计数，不阻止对象被回收

class CacheEntry:
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __repr__(self):
        return f"CacheEntry({self.key!r}, {self.value!r})"

    def __del__(self):
        print(f"  CacheEntry({self.key!r}) 被回收")

print("创建对象并建立弱引用:")
entry = CacheEntry("user_1", {"name": "Alice"})
weak = weakref.ref(entry)

print(f"  strong ref: {entry}")
print(f"  weak ref(): {weak()}")
print(f"  refcount:   {sys.getrefcount(entry)}")

print("\n删除强引用:")
del entry
print(f"  weak ref(): {weak()}")  # None — 对象已被回收

print("\n=== WeakValueDictionary — 弱引用缓存 ===")
# 实际应用：缓存中的对象可以被自动回收

class ExpensiveObject:
    def __init__(self, key):
        self.key = key
    def __repr__(self):
        return f"Expensive({self.key})"

cache = weakref.WeakValueDictionary()

# 创建对象并放入缓存
obj1 = ExpensiveObject("data_1")
obj2 = ExpensiveObject("data_2")
cache["data_1"] = obj1
cache["data_2"] = obj2

print(f"缓存中: {list(cache.keys())}")

# 删除强引用
del obj1
gc.collect()
print(f"del obj1 后: {list(cache.keys())}")  # data_1 自动从缓存消失

del obj2
gc.collect()
print(f"del obj2 后: {list(cache.keys())}")

print("\n=== __del__ 的注意事项 ===")
print("""
⚠️ C++ 开发者注意:
1. __del__ 不等于析构函数
   - 调用时机不确定（GC 决定）
   - 循环引用中可能不被调用
   - 解释器退出时可能跳过

2. 不要在 __del__ 中做资源清理
   - 使用 context manager (with 语句) 代替
   - 使用 atexit 模块处理退出清理

3. __del__ 中不要访问全局变量
   - 解释器退出时全局变量可能已被删除
""".strip())
