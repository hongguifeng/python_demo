"""
继承与 MRO (Method Resolution Order)

C++ 的多重继承有菱形继承问题（Diamond Problem）。
Python 用 C3 线性化算法解决。
"""

print("=== 基本继承 ===")

class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        raise NotImplementedError("子类必须实现 speak()")

    def __repr__(self):
        return f"{type(self).__name__}({self.name!r})"

class Dog(Animal):
    def speak(self):
        return f"{self.name} says Woof!"

class Cat(Animal):
    def speak(self):
        return f"{self.name} says Meow!"

# 多态（和 C++ 虚函数一样，但不需要 virtual 关键字）
animals = [Dog("Buddy"), Cat("Whiskers"), Dog("Rex")]
for animal in animals:
    print(f"  {animal}: {animal.speak()}")

print(f"\nisinstance(Dog('X'), Animal): {isinstance(Dog('X'), Animal)}")

print("\n=== 多重继承与 MRO ===")

class A:
    def method(self):
        print("    A.method")

class B(A):
    def method(self):
        print("    B.method")
        super().method()  # 调用 MRO 中的下一个

class C(A):
    def method(self):
        print("    C.method")
        super().method()

class D(B, C):  # 菱形继承！
    def method(self):
        print("    D.method")
        super().method()

d = D()
print("调用 D().method():")
d.method()

# 查看 MRO
print(f"\nMRO: {[cls.__name__ for cls in D.__mro__]}")
# D → B → C → A → object
# C3 线性化保证每个类只被调用一次

print("\n=== super() 详解 ===")
# super() 不是调用"父类"，而是调用 MRO 中的"下一个类"
# 这和 C++ 的直接调用 Base::method() 不同

class Base:
    def __init__(self):
        print("    Base.__init__")

class Left(Base):
    def __init__(self):
        print("    Left.__init__")
        super().__init__()  # 不一定调用 Base！

class Right(Base):
    def __init__(self):
        print("    Right.__init__")
        super().__init__()

class Child(Left, Right):
    def __init__(self):
        print("    Child.__init__")
        super().__init__()

print("创建 Child():")
Child()
print(f"MRO: {[c.__name__ for c in Child.__mro__]}")

print("\n=== Mixin 模式 ===")
# Python 多重继承的最佳实践：Mixin
# Mixin 是只提供方法、不提供数据的类

class JsonMixin:
    """提供 JSON 序列化能力"""
    def to_json(self):
        import json
        return json.dumps(self.__dict__, default=str)

class PrintableMixin:
    """提供友好的打印"""
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{type(self).__name__}({attrs})"

class User(JsonMixin, PrintableMixin):
    def __init__(self, name, email):
        self.name = name
        self.email = email

user = User("Alice", "alice@example.com")
print(f"repr:  {user}")
print(f"json:  {user.to_json()}")

print("\n=== 抽象基类 (ABC) — 类似 C++ 的纯虚函数 ===")
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self) -> float:
        """必须由子类实现（类似 virtual ... = 0）"""
        ...

    @abstractmethod
    def perimeter(self) -> float:
        ...

    def describe(self):
        """非抽象方法可以有默认实现"""
        return f"{type(self).__name__}: area={self.area():.2f}"

# shape = Shape()  # TypeError: 不能实例化抽象类

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(3, 4)
print(f"{rect.describe()}, perimeter={rect.perimeter():.2f}")
