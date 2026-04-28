"""
动态类创建与修改

Python 的类可以在运行时创建、修改、甚至删除。
这在 C++ 中是完全不可能的。
"""

print("=== 动态创建类 ===")

def make_dataclass(name, fields):
    """简化的 dataclass 工厂"""
    def __init__(self, **kwargs):
        for field in fields:
            setattr(self, field, kwargs.get(field))

    def __repr__(self):
        attrs = ", ".join(f"{f}={getattr(self, f)!r}" for f in fields)
        return f"{name}({attrs})"

    cls = type(name, (), {
        '__init__': __init__,
        '__repr__': __repr__,
        '_fields': fields,
    })
    return cls

# 运行时创建类
Point = make_dataclass("Point", ["x", "y"])
Color = make_dataclass("Color", ["r", "g", "b"])

p = Point(x=1, y=2)
c = Color(r=255, g=128, b=0)
print(f"动态类: {p}")
print(f"动态类: {c}")

print("\n=== 猴子补丁 (Monkey Patching) ===")
# 运行时修改现有类（慎用！主要用于测试和热修复）

class Calculator:
    def add(self, a, b):
        return a + b

    def multiply(self, a, b):
        return a * b

calc = Calculator()
print(f"原始: calc.add(1, 2) = {calc.add(1, 2)}")

# 运行时添加方法
def subtract(self, a, b):
    return a - b

Calculator.subtract = subtract
print(f"补丁后: calc.subtract(5, 3) = {calc.subtract(5, 3)}")

# 替换方法（常用于测试中的 mock）
original_add = Calculator.add

def logged_add(self, a, b):
    result = original_add(self, a, b)
    print(f"  [log] add({a}, {b}) = {result}")
    return result

Calculator.add = logged_add
calc.add(3, 4)

# 恢复
Calculator.add = original_add

print("\n=== 装饰器 vs 元类 vs __init_subclass__ ===")
# 三种方式实现"自动注册"

# 方式 1: 装饰器
registry_decorator = {}

def register(cls):
    registry_decorator[cls.__name__] = cls
    return cls

@register
class HandlerA:
    pass

@register
class HandlerB:
    pass

print(f"装饰器注册: {list(registry_decorator.keys())}")

# 方式 2: __init_subclass__（推荐）
class Base:
    _registry = {}
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Base._registry[cls.__name__] = cls

class HandlerC(Base):
    pass

class HandlerD(Base):
    pass

print(f"__init_subclass__ 注册: {list(Base._registry.keys())}")

print("\n=== __getattr__ 实现代理模式 ===")

class LoggingProxy:
    """透明代理 — 记录所有方法调用"""

    def __init__(self, target):
        self._target = target
        self._log = []

    def __getattr__(self, name):
        attr = getattr(self._target, name)
        if callable(attr):
            def logged(*args, **kwargs):
                self._log.append((name, args, kwargs))
                return attr(*args, **kwargs)
            return logged
        return attr

# 代理一个列表
proxied_list = LoggingProxy([])
proxied_list.append(1)
proxied_list.append(2)
proxied_list.extend([3, 4])
print(f"代理列表: {proxied_list._target}")
print(f"操作日志: {proxied_list._log}")

print("\n=== exec/eval — 最极端的动态性 ===")
# 类似 C 中没有的概念（除非嵌入脚本引擎）

# eval: 执行表达式
result = eval("2 ** 10 + 1")
print(f"eval('2**10+1') = {result}")

# exec: 执行语句
namespace = {}
exec("""
def generated_func(x):
    return x ** 2 + 1
""", namespace)

func = namespace['generated_func']
print(f"exec 生成的函数: func(5) = {func(5)}")

# ⚠️ 安全警告: 永远不要对用户输入使用 eval/exec！
print("\n⚠️  eval/exec 有严重的安全风险，不要对不信任的输入使用")
