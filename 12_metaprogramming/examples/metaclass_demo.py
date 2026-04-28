"""
元类 (Metaclass) — "类的类"

在 Python 中:
  - 对象是类的实例
  - 类是元类的实例
  - 默认元类是 type

类比:
  C++ 的 class 定义在编译时固定
  Python 的 class 在运行时由元类动态创建
"""

print("=== 类也是对象 ===")

class Dog:
    species = "Canis familiaris"

# Dog 本身是一个对象
print(f"Dog 的类型: {type(Dog)}")  # <class 'type'>
print(f"Dog 的类型的类型: {type(type(Dog))}")  # <class 'type'>

# type 是自己的类型！
print(f"type(type) = {type(type)}")

print("\n=== type() 动态创建类 ===")
# type(name, bases, dict) 可以在运行时创建类
# 这等价于 class 语句！

# 用 class 语句:
class Point1:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __repr__(self):
        return f"Point1({self.x}, {self.y})"

# 用 type() 等价创建:
Point2 = type('Point2', (), {
    '__init__': lambda self, x, y: setattr(self, 'x', x) or setattr(self, 'y', y),
    '__repr__': lambda self: f"Point2({self.x}, {self.y})"
})

p1 = Point1(1, 2)
p2 = Point2(3, 4)
print(f"class 语句: {p1}")
print(f"type() 创建: {p2}")

print("\n=== 自定义元类 ===")

class ValidatedMeta(type):
    """元类：在创建类时自动验证"""

    def __new__(mcs, name, bases, namespace):
        # 在类创建时执行检查
        cls = super().__new__(mcs, name, bases, namespace)

        # 确保所有公开方法都有 docstring
        for attr_name, attr_value in namespace.items():
            if callable(attr_value) and not attr_name.startswith('_'):
                if not attr_value.__doc__:
                    print(f"  ⚠ {name}.{attr_name}() 缺少 docstring")

        return cls

class MyService(metaclass=ValidatedMeta):
    def process(self):
        """处理数据"""
        return "processed"

    def validate(self):  # 没有 docstring — 元类会警告
        return True

    def _internal(self):  # 私有方法不检查
        pass

print(f"MyService 的元类: {type(MyService)}")

print("\n=== 实用元类：单例模式 ===")

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class Database(metaclass=SingletonMeta):
    def __init__(self):
        self.connection = "connected"
        print("  Database 初始化（只会执行一次）")

db1 = Database()
db2 = Database()
print(f"db1 is db2: {db1 is db2}")

print("\n=== __init_subclass__ — 元类的简化替代 ===")
# Python 3.6+ 推荐用这个代替简单的元类

class Plugin:
    """插件基类 — 自动注册子类"""
    _registry: dict = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        name = cls.__name__.lower()
        Plugin._registry[name] = cls
        print(f"  注册插件: {name}")

class JSONPlugin(Plugin):
    def process(self):
        return "json"

class XMLPlugin(Plugin):
    def process(self):
        return "xml"

class CSVPlugin(Plugin):
    def process(self):
        return "csv"

print(f"已注册的插件: {list(Plugin._registry.keys())}")

# 动态实例化
for name, cls in Plugin._registry.items():
    instance = cls()
    print(f"  {name}.process() = {instance.process()}")

print("\n=== __class_getitem__ — 泛型语法支持 ===")

class TypedList:
    """支持 TypedList[int] 语法"""
    def __class_getitem__(cls, item):
        print(f"  TypedList[{item.__name__}] 被调用")
        return cls  # 简化实现

TypedList[int]
TypedList[str]
