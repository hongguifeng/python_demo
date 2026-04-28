"""
ctypes — 从 Python 调用 C 动态库

不需要编译步骤，直接加载 .so/.dll/.dylib
"""

import ctypes
import ctypes.util
import struct
import sys

print("=== 加载系统 C 库 ===")

# 加载 libc（所有系统都有）
if sys.platform == "linux":
    libc = ctypes.CDLL("libc.so.6")
elif sys.platform == "darwin":
    libc = ctypes.CDLL("libc.dylib")
else:
    libc = ctypes.cdll.msvcrt

# 调用 C 函数
# C: int abs(int x);
print(f"libc.abs(-42) = {libc.abs(-42)}")

# C: time_t time(time_t *t);
libc.time.restype = ctypes.c_int64
print(f"libc.time(NULL) = {libc.time(None)}")

print("\n=== 查找库路径 ===")
# 类似 ldconfig / pkg-config
math_lib = ctypes.util.find_library("m")
print(f"libm 路径: {math_lib}")

c_lib = ctypes.util.find_library("c")
print(f"libc 路径: {c_lib}")

print("\n=== 类型映射 ===")
print("""
C 类型          ctypes 类型        Python 类型
-------         ------------       -----------
char            c_char             bytes
int             c_int              int
long            c_long             int
float           c_float            float
double          c_double           float
char*           c_char_p           bytes
void*           c_void_p           int/None
int*            POINTER(c_int)     ctypes 指针
""".strip())

print("\n\n=== 加载 libm 并调用数学函数 ===")

if sys.platform == "linux":
    libm = ctypes.CDLL("libm.so.6")
elif sys.platform == "darwin":
    libm = ctypes.CDLL("libm.dylib")
else:
    libm = libc  # Windows 的 msvcrt 包含数学函数

# 必须声明参数和返回类型！否则 Python 假设 int
libm.sqrt.argtypes = [ctypes.c_double]
libm.sqrt.restype = ctypes.c_double

libm.pow.argtypes = [ctypes.c_double, ctypes.c_double]
libm.pow.restype = ctypes.c_double

print(f"libm.sqrt(2.0) = {libm.sqrt(2.0)}")
print(f"libm.pow(2.0, 10.0) = {libm.pow(2.0, 10.0)}")

print("\n=== 结构体 ===")

# C:
# struct Point {
#     double x;
#     double y;
# };

class Point(ctypes.Structure):
    _fields_ = [
        ("x", ctypes.c_double),
        ("y", ctypes.c_double),
    ]

    def __repr__(self):
        return f"Point({self.x}, {self.y})"

p = Point(3.0, 4.0)
print(f"结构体: {p}")
print(f"sizeof(Point) = {ctypes.sizeof(p)} bytes")
print(f"x offset = {Point.x.offset}, y offset = {Point.y.offset}")

# 结构体数组
PointArray = Point * 3
points = PointArray(Point(1, 1), Point(2, 2), Point(3, 3))
for p in points:
    print(f"  {p}")

print("\n=== 指针操作 ===")

# C: int value = 42; int *ptr = &value;
value = ctypes.c_int(42)
ptr = ctypes.pointer(value)
print(f"值: {value.value}")
print(f"指针解引用: {ptr.contents.value}")
print(f"通过指针修改...")
ptr.contents.value = 100
print(f"修改后: {value.value}")

# 数组（连续内存）
IntArray = ctypes.c_int * 5
arr = IntArray(10, 20, 30, 40, 50)
print(f"\n数组: {list(arr)}")
print(f"arr[2] = {arr[2]}")

print("\n=== 回调函数 ===")
# C 调用 Python 函数（通过函数指针）

# C: typedef int (*compare_func)(const void*, const void*);
COMPARE_FUNC = ctypes.CFUNCTYPE(ctypes.c_int,
                                 ctypes.POINTER(ctypes.c_int),
                                 ctypes.POINTER(ctypes.c_int))

def py_compare(a, b):
    """Python 回调函数，传给 C 的 qsort"""
    return a[0] - b[0]

c_compare = COMPARE_FUNC(py_compare)

# 使用 libc.qsort
arr = (ctypes.c_int * 6)(5, 3, 1, 4, 2, 6)
print(f"排序前: {list(arr)}")

libc.qsort(arr,
            len(arr),
            ctypes.sizeof(ctypes.c_int),
            c_compare)

print(f"排序后: {list(arr)}")

print("\n=== 性能注意事项 ===")
print("""
ctypes 的开销:
  - 每次调用有类型转换开销
  - 不适合频繁调用简单函数
  - 适合调用执行时间较长的函数

如果需要更高性能:
  - cffi: 更现代，JIT 友好（PyPy 推荐）
  - pybind11: C++ 绑定首选
  - Cython: 将 Python 编译为 C
""".strip())
