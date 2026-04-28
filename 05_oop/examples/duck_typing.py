"""
鸭子类型 (Duck Typing)

"If it walks like a duck and quacks like a duck, it's a duck."

C++ 的多态需要继承层次和虚函数。
Python 只关心对象有没有需要的方法/属性。
"""

print("=== 鸭子类型基础 ===")

# 这个函数不关心参数的类型，只关心它有没有 read() 方法
def read_data(source):
    """读取数据 — source 可以是任何有 read() 方法的对象"""
    return source.read()

# 不同的"鸭子"，没有共同基类
class FileSource:
    def __init__(self, content):
        self.content = content
    def read(self):
        return self.content

class NetworkSource:
    def __init__(self, data):
        self.data = data
    def read(self):
        return self.data

class DatabaseSource:
    def __init__(self, records):
        self.records = records
    def read(self):
        return str(self.records)

# 它们都能传给 read_data，不需要继承同一个接口
for source in [FileSource("file content"),
               NetworkSource("network data"),
               DatabaseSource([1, 2, 3])]:
    print(f"  {type(source).__name__}: {read_data(source)}")

print("\n=== 内置协议就是鸭子类型 ===")

class Deck:
    """一副扑克牌 — 实现了序列协议（__len__ + __getitem__）"""
    ranks = "2 3 4 5 6 7 8 9 10 J Q K A".split()
    suits = "♠ ♥ ♦ ♣".split()

    def __init__(self):
        self.cards = [f"{r}{s}" for s in self.suits for r in self.ranks]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, index):
        return self.cards[index]

deck = Deck()
print(f"牌数: {len(deck)}")
print(f"第一张: {deck[0]}")
print(f"最后一张: {deck[-1]}")
print(f"前3张: {deck[:3]}")

# 因为实现了 __getitem__，自动获得迭代能力！
print(f"随机抽: ", end="")
import random
print(random.choice(deck))

# in 运算符也自动可用
print(f"'A♠' in deck: {'A♠' in deck}")

print("\n=== Protocol（Python 3.8+）— 结构化鸭子类型 ===")
from typing import Protocol, runtime_checkable

@runtime_checkable
class Drawable(Protocol):
    """定义一个协议 — 类似 C++ 的 Concept (C++20)
    不需要继承，只要有 draw() 方法就行"""
    def draw(self) -> str: ...

class Circle:
    def __init__(self, r):
        self.r = r
    def draw(self) -> str:
        return f"○ (r={self.r})"

class Square:
    def __init__(self, s):
        self.s = s
    def draw(self) -> str:
        return f"□ (s={self.s})"

class NotDrawable:
    pass

# 运行时检查
print(f"Circle 是 Drawable: {isinstance(Circle(5), Drawable)}")
print(f"Square 是 Drawable: {isinstance(Square(3), Drawable)}")
print(f"NotDrawable 是 Drawable: {isinstance(NotDrawable(), Drawable)}")

# 使用
def render(shapes: list[Drawable]):
    for shape in shapes:
        print(f"  绘制: {shape.draw()}")

render([Circle(5), Square(3)])

print("\n=== EAFP vs LBYL ===")
# C++ 风格 (LBYL - Look Before You Leap):
#   if (ptr != nullptr) { ptr->method(); }

# Python 风格 (EAFP - Easier to Ask Forgiveness than Permission):
#   try: obj.method() except AttributeError: ...

class Config:
    def __init__(self, data):
        self.__dict__.update(data)

config = Config({"host": "localhost", "port": 8080})

# LBYL (C 风格 — 在 Python 中不推荐)
if hasattr(config, 'timeout'):
    timeout = config.timeout
else:
    timeout = 30
print(f"LBYL timeout: {timeout}")

# EAFP (Python 风格 — 推荐)
try:
    timeout = config.timeout
except AttributeError:
    timeout = 30
print(f"EAFP timeout: {timeout}")

# 最 Pythonic: getattr
timeout = getattr(config, 'timeout', 30)
print(f"getattr timeout: {timeout}")
