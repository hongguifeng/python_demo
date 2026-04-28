"""
引用计数 — CPython 的主要内存管理机制

类似 C++ 的 shared_ptr，但完全自动。
"""

import sys
import ctypes

print("=== 引用计数基础 ===")
# sys.getrefcount() 返回引用计数（会多 1，因为参数传递本身增加引用）

a = [1, 2, 3]
print(f"创建后:         refcount = {sys.getrefcount(a)}")  # 2 (a + getrefcount 参数)

b = a
print(f"b = a 后:       refcount = {sys.getrefcount(a)}")  # 3

c = a
print(f"c = a 后:       refcount = {sys.getrefcount(a)}")  # 4

lst = [a, a, a]
print(f"列表中3个引用后: refcount = {sys.getrefcount(a)}")  # 7

del c
print(f"del c 后:       refcount = {sys.getrefcount(a)}")  # 6

lst.clear()
print(f"lst.clear() 后: refcount = {sys.getrefcount(a)}")  # 3

del b
print(f"del b 后:       refcount = {sys.getrefcount(a)}")  # 2

print("\n=== 引用计数归零 → 立即销毁 ===")
class Tracked:
    def __init__(self, name):
        self.name = name
        print(f"  + 创建 {self.name}")

    def __del__(self):
        print(f"  - 销毁 {self.name}")

print("演示确定性销毁:")
obj = Tracked("A")
print("  准备删除引用...")
del obj  # CPython 中，引用计数归零，立即调用 __del__
print("  删除完成")

print("\n重新赋值触发销毁:")
obj = Tracked("B")
obj = Tracked("C")  # B 的引用计数归零，立即销毁
del obj

print("\n=== 小整数缓存 ===")
# CPython 预缓存 -5 到 256 的整数对象
# 这是性能优化，意味着这些整数是单例

a = 256
b = 256
print(f"256 is 256: {a is b} (缓存)")

# 较大的整数不被缓存（在交互模式中）
# 注意：在脚本中，编译器可能会优化常量折叠

print(f"\n整数 42 的引用计数: {sys.getrefcount(42)} (很多内部引用)")
print(f"整数 12345678 的引用计数: {sys.getrefcount(12345678)}")

print("\n=== 字符串驻留 (Interning) ===")
# 类似小整数缓存，短字符串也会被缓存
a = "hello"
b = "hello"
print(f'"hello" is "hello": {a is b} (驻留)')

# 包含特殊字符的通常不驻留
a = "hello world!"
b = "hello world!"
print(f'"hello world!" is "hello world!": {a is b}')

# 可以手动驻留
a = sys.intern("hello world!")
b = sys.intern("hello world!")
print(f'intern 后: {a is b}')

print("\n=== 对象内存布局 (C 开发者视角) ===")
# 每个 Python 对象在 C 层面是:
# typedef struct {
#     Py_ssize_t ob_refcnt;    // 引用计数
#     PyTypeObject *ob_type;   // 类型指针
#     ...                      // 具体数据
# } PyObject;

x = 42
print(f"int 42:")
print(f"  id (地址): {id(x):#x}")
print(f"  type:      {type(x)}")
print(f"  size:      {sys.getsizeof(x)} bytes")

x = []
print(f"\n空 list:")
print(f"  size: {sys.getsizeof(x)} bytes (含 ob_refcnt + ob_type + 列表头)")

print(f"\n对象大小对比:")
objects = [
    ("int(0)", 0),
    ("int(2^30)", 2**30),
    ("int(2^100)", 2**100),
    ("float(0.0)", 0.0),
    ("str('')", ""),
    ("str('hello')", "hello"),
    ("list([])", []),
    ("list([0]*10)", [0]*10),
    ("dict({})", {}),
    ("tuple(())", ()),
    ("set()", set()),
]
for name, obj in objects:
    print(f"  {name:25s} {sys.getsizeof(obj):6d} bytes")
