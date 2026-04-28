"""
魔术方法 (Dunder Methods) — Python 的运算符重载

C++ 用 operator+, operator== 等。
Python 用 __add__, __eq__ 等双下划线方法。
"""

print("=== 实现一个完整的 Vector 类 ===")

class Vector:
    """二维向量 — 展示 Python 运算符重载"""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # 字符串表示 — 类似 C++ 的 operator<<
    def __repr__(self):
        """开发用表示（应能重建对象）"""
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        """用户友好表示"""
        return f"({self.x}, {self.y})"

    # 算术运算符 — 类似 C++ 的 operator+
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        """向量 * 标量"""
        return Vector(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar):
        """标量 * 向量（反向乘法）— C++ 需要友元函数"""
        return self.__mul__(scalar)

    def __neg__(self):
        return Vector(-self.x, -self.y)

    def __abs__(self):
        """abs() 内置函数"""
        return (self.x**2 + self.y**2) ** 0.5

    # 比较运算符 — 类似 C++20 的 operator<=>
    def __eq__(self, other):
        if not isinstance(other, Vector):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        """实现了 __eq__ 就必须实现 __hash__（否则变成不可哈希）"""
        return hash((self.x, self.y))

    # 容器协议
    def __len__(self):
        return 2

    def __getitem__(self, index):
        """支持 v[0], v[1]"""
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        raise IndexError(f"Vector index {index} out of range")

    def __iter__(self):
        """支持 for x in v / 解包"""
        yield self.x
        yield self.y

    # 布尔值
    def __bool__(self):
        """零向量为 False"""
        return self.x != 0 or self.y != 0

    # 格式化
    def __format__(self, fmt):
        """支持 format() 和 f-string 格式"""
        if fmt == 'p':  # 极坐标
            import math
            r = abs(self)
            theta = math.atan2(self.y, self.x)
            return f"({r:.2f}, {math.degrees(theta):.1f}°)"
        return f"({self.x:{fmt}}, {self.y:{fmt}})"

# 使用
v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1!r}")          # __repr__
print(f"v2 = {v2}")            # __str__
print(f"v1 + v2 = {v1 + v2}")  # __add__
print(f"v1 - v2 = {v1 - v2}")  # __sub__
print(f"v1 * 3  = {v1 * 3}")   # __mul__
print(f"3 * v1  = {3 * v1}")   # __rmul__
print(f"-v1     = {-v1}")       # __neg__
print(f"|v1|    = {abs(v1)}")   # __abs__
print(f"v1 == v2: {v1 == v2}")  # __eq__
print(f"v1[0]   = {v1[0]}")    # __getitem__
print(f"len(v1) = {len(v1)}")  # __len__

# 解包（__iter__）
x, y = v1
print(f"解包: x={x}, y={y}")

# 格式化
print(f"默认:   {v1}")
print(f"浮点:   {v1:.2f}")
print(f"极坐标: {v1:p}")

# 可以用作 dict key（因为实现了 __hash__）
vector_names = {Vector(1, 0): "east", Vector(0, 1): "north"}
print(f"\nvector_names[Vector(1,0)] = {vector_names[Vector(1, 0)]}")

print("\n=== 上下文管理器协议 ===")

class Timer:
    """类似 C++ 的 RAII 计时器"""
    def __enter__(self):
        import time
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import time
        self.elapsed = time.perf_counter() - self.start
        print(f"  耗时: {self.elapsed:.6f}s")
        return False  # 不抑制异常

with Timer():
    total = sum(range(1_000_000))
    print(f"  结果: {total}")

print("\n=== callable 协议 ===")

class Adder:
    """可调用对象 — 类似 C++ 的仿函数 (functor)"""
    def __init__(self, n):
        self.n = n

    def __call__(self, x):
        return self.n + x

add5 = Adder(5)
print(f"add5(3) = {add5(3)}")
print(f"callable(add5) = {callable(add5)}")
