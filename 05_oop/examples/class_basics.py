"""
Python 类基础 — 与 C++ 的对比

C++ class 是编译时确定的内存布局。
Python class 是运行时动态的对象。
"""

print("=== 基本类定义 ===")

class Point:
    """
    C++ 等价:
    class Point {
    public:
        double x, y;
        Point(double x, double y) : x(x), y(y) {}
    };
    """
    # 类变量（类似 C++ 的 static 成员）
    dimension = 2

    def __init__(self, x, y):
        """构造函数（但实际上是初始化器，__new__ 才是构造）"""
        self.x = x  # 实例变量（self 类似 C++ 的 this）
        self.y = y

    def distance_to(self, other):
        """实例方法 — self 是显式的（C++ 的 this 是隐式的）"""
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

    def __repr__(self):
        """类似 C++ 的 operator<<(ostream&)"""
        return f"Point({self.x}, {self.y})"

p1 = Point(3, 4)
p2 = Point(0, 0)
print(f"p1 = {p1}")
print(f"p2 = {p2}")
print(f"距离: {p1.distance_to(p2):.2f}")
print(f"维度: {Point.dimension}")

print("\n=== 没有真正的 private ===")

class Account:
    def __init__(self, owner, balance):
        self.owner = owner       # public
        self._balance = balance  # "protected"（约定，不强制）
        self.__id = id(self)     # "private"（名称修饰 name mangling）

    def get_info(self):
        return f"{self.owner}: ${self._balance}"

acc = Account("Alice", 1000)
print(f"public: {acc.owner}")
print(f"'protected': {acc._balance}")  # 可以访问，但不应该
# print(acc.__id)  # AttributeError!
print(f"'private' (mangled): {acc._Account__id}")  # 通过修饰名仍可访问

# Python 哲学："We are all consenting adults"
# 信任使用者而非强制封装

print("\n=== 类是动态的 ===")

# 可以在运行时给实例添加属性（C++ 绝不可能！）
p = Point(1, 2)
p.z = 3  # 动态添加属性
print(f"p.z = {p.z}")
print(f"p.__dict__ = {p.__dict__}")

# 甚至可以给类添加方法
def magnitude(self):
    return (self.x**2 + self.y**2) ** 0.5

Point.magnitude = magnitude  # 动态添加方法
print(f"p1.magnitude() = {p1.magnitude():.2f}")

print("\n=== __slots__ — 限制动态属性 ===")

class FixedPoint:
    """使用 __slots__ 限制属性（类似 C struct 的固定布局）
    优点：
    1. 省内存（不需要 __dict__）
    2. 更快的属性访问
    3. 防止拼写错误
    """
    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

fp = FixedPoint(1, 2)
# fp.z = 3  # AttributeError! 不能添加 slots 之外的属性

import sys
print(f"\n普通 Point 实例大小:    {sys.getsizeof(p1) + sys.getsizeof(p1.__dict__)} bytes (含 __dict__)")
print(f"FixedPoint 实例大小:   {sys.getsizeof(fp)} bytes (无 __dict__)")

print("\n=== 类方法 vs 静态方法 ===")

class Date:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __repr__(self):
        return f"Date({self.year}, {self.month}, {self.day})"

    @classmethod
    def from_string(cls, date_str):
        """类方法：接收类本身作为第一个参数
        类似 C++ 的命名构造函数（Named Constructor）"""
        year, month, day = map(int, date_str.split('-'))
        return cls(year, month, day)

    @classmethod
    def today(cls):
        import datetime
        d = datetime.date.today()
        return cls(d.year, d.month, d.day)

    @staticmethod
    def is_valid(year, month, day):
        """静态方法：不接收 self 或 cls
        和 C++ 的 static 方法一样"""
        return 1 <= month <= 12 and 1 <= day <= 31

d1 = Date(2024, 1, 15)
d2 = Date.from_string("2024-06-20")
d3 = Date.today()
print(f"d1 = {d1}")
print(f"d2 = {d2}")
print(f"d3 = {d3}")
print(f"Date.is_valid(2024, 13, 1) = {Date.is_valid(2024, 13, 1)}")
