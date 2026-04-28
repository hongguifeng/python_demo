"""
dataclass — 现代 Python 的 struct

Python 3.7+ 引入，自动生成 __init__, __repr__, __eq__ 等。
类比 C 的 struct 或 C++20 的聚合类。
"""

from dataclasses import dataclass, field, asdict, astuple
from typing import ClassVar

print("=== 基本 dataclass ===")

@dataclass
class Point:
    """
    自动生成:
    - __init__(self, x, y)
    - __repr__(self)
    - __eq__(self, other)
    """
    x: float
    y: float

p1 = Point(3.0, 4.0)
p2 = Point(3.0, 4.0)
print(f"p1 = {p1}")
print(f"p1 == p2: {p1 == p2}")

print("\n=== 默认值和工厂 ===")

@dataclass
class Config:
    host: str = "localhost"
    port: int = 8080
    tags: list[str] = field(default_factory=list)  # 可变默认值必须用 field
    _connections: int = field(default=0, repr=False)  # 不出现在 repr 中

    # 类变量（不是实例字段）
    MAX_CONNECTIONS: ClassVar[int] = 100

c = Config()
print(f"默认: {c}")
c2 = Config("example.com", 443, ["prod", "api"])
print(f"自定义: {c2}")

print("\n=== 不可变 dataclass (frozen) ===")

@dataclass(frozen=True)  # 类似 C++ 的 const struct
class Color:
    r: int
    g: int
    b: int

    @property
    def hex(self):
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

red = Color(255, 0, 0)
print(f"red = {red}, hex = {red.hex}")
# red.r = 128  # FrozenInstanceError!

# frozen dataclass 可以作为 dict key 和 set 元素
colors = {Color(255, 0, 0): "red", Color(0, 255, 0): "green"}
print(f"颜色字典: {colors}")

print("\n=== 排序支持 ===")

@dataclass(order=True)  # 自动生成 __lt__, __le__, __gt__, __ge__
class Version:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"v{self.major}.{self.minor}.{self.patch}"

versions = [Version(2, 0, 0), Version(1, 9, 1), Version(1, 10, 0)]
versions.sort()
print(f"排序: {[str(v) for v in versions]}")

print("\n=== 继承 ===")

@dataclass
class Shape:
    color: str = "black"

@dataclass
class Circle(Shape):
    radius: float = 1.0

    @property
    def area(self):
        import math
        return math.pi * self.radius ** 2

c = Circle(color="red", radius=5.0)
print(f"circle = {c}, area = {c.area:.2f}")

print("\n=== __post_init__ — 初始化后处理 ===")

@dataclass
class Employee:
    first_name: str
    last_name: str
    salary: float
    full_name: str = field(init=False)  # 不在 __init__ 参数中

    def __post_init__(self):
        self.full_name = f"{self.first_name} {self.last_name}"
        if self.salary < 0:
            raise ValueError("工资不能为负")

emp = Employee("Alice", "Smith", 50000)
print(f"employee = {emp}")

print("\n=== 转换工具 ===")
p = Point(3.0, 4.0)
print(f"asdict:  {asdict(p)}")
print(f"astuple: {astuple(p)}")

print("\n=== 对比传统写法 ===")
print("""
传统类需要手写:
  class Point:
      def __init__(self, x, y):
          self.x = x
          self.y = y
      def __repr__(self):
          return f"Point({self.x}, {self.y})"
      def __eq__(self, other):
          return self.x == other.x and self.y == other.y
      def __hash__(self):
          return hash((self.x, self.y))

dataclass 一行搞定:
  @dataclass(frozen=True)
  class Point:
      x: float
      y: float
""".strip())
