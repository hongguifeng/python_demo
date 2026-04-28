"""
描述符 (Descriptor) — Python 属性访问的底层机制

描述符是实现了 __get__/__set__/__delete__ 的对象。
@property、@classmethod、@staticmethod 都是描述符。

类比 C++: 类似于重载 operator. 和 operator=
"""

print("=== 描述符协议 ===")

class Validated:
    """数据验证描述符 — 类似 C++ 中重载 setter 的属性"""

    def __init__(self, name, validator):
        self.name = name
        self.validator = validator

    def __set_name__(self, owner, name):
        """Python 3.6+: 自动获取属性名"""
        self.storage_name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.storage_name, None)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.name}: invalid value {value!r}")
        setattr(obj, self.storage_name, value)

class Person:
    name = Validated("name", lambda v: isinstance(v, str) and len(v) > 0)
    age = Validated("age", lambda v: isinstance(v, int) and 0 <= v <= 150)

p = Person()
p.name = "Alice"
p.age = 30
print(f"p.name = {p.name}, p.age = {p.age}")

try:
    p.age = -5
except ValueError as e:
    print(f"验证失败: {e}")

try:
    p.name = ""
except ValueError as e:
    print(f"验证失败: {e}")

print("\n=== @property 的本质 ===")
# @property 就是一个描述符类

class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("温度不能低于绝对零度")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

t = Temperature(100)
print(f"\n{t.celsius}°C = {t.fahrenheit}°F")
t.fahrenheit = 32
print(f"{t.celsius}°C = {t.fahrenheit}°F")

print("\n=== 实现 @property 的简化版 ===")

class MyProperty:
    """property 描述符的简化实现"""

    def __init__(self, fget=None, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError("不可读")
        return self.fget(obj)

    def __set__(self, obj, value):
        if self.fset is None:
            raise AttributeError("不可写")
        self.fset(obj, value)

    def setter(self, fset):
        return MyProperty(self.fget, fset)

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @MyProperty
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        self._radius = value

    @MyProperty
    def area(self):
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(f"radius = {c.radius}, area = {c.area:.2f}")
c.radius = 10
print(f"radius = {c.radius}, area = {c.area:.2f}")

print("\n=== __getattr__ 和 __getattribute__ ===")

class DotDict:
    """像 JavaScript 对象一样用点号访问字典"""

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        """当常规属性查找失败时调用"""
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(f"no attribute {name!r}")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._data[name] = value

config = DotDict({"host": "localhost", "port": 8080})
print(f"\nconfig.host = {config.host}")
print(f"config.port = {config.port}")
config.debug = True
print(f"config.debug = {config.debug}")

print("\n=== 缓存属性描述符 ===")

class CachedProperty:
    """计算一次后缓存结果（类似 functools.cached_property）"""

    def __init__(self, func):
        self.func = func
        self.attr_name = func.__name__

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        value = self.func(obj)
        # 直接设置实例属性，下次访问不经过描述符
        setattr(obj, self.attr_name, value)
        return value

class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    @CachedProperty
    def statistics(self):
        """耗时计算，只执行一次"""
        print("  [计算统计信息...]")
        return {
            "mean": sum(self.data) / len(self.data),
            "min": min(self.data),
            "max": max(self.data),
        }

analyzer = DataAnalyzer([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
print(f"第一次: {analyzer.statistics}")  # 会打印 "计算..."
print(f"第二次: {analyzer.statistics}")  # 直接返回缓存
