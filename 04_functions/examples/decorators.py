"""
装饰器 (Decorators) — Python 最优雅的元编程工具

类比：
- C 的宏 — 但类型安全、可组合
- C++ 的模板 — 但运行时、更灵活
- AOP (面向切面编程) — 但语法内建
"""

import time
import functools

print("=== 装饰器本质 ===")

# 装饰器就是一个接收函数并返回函数的函数
def my_decorator(func):
    @functools.wraps(func)  # 保留原函数的元信息
    def wrapper(*args, **kwargs):
        print(f"  [before] 调用 {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  [after]  {func.__name__} 返回 {result}")
        return result
    return wrapper

@my_decorator  # 语法糖，等价于: greet = my_decorator(greet)
def greet(name):
    return f"Hello, {name}!"

print(greet("World"))
print(f"函数名保持: {greet.__name__}")  # 'greet' 不是 'wrapper'

print("\n=== 实用装饰器：计时器 ===")

def timer(func):
    """测量函数执行时间"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} 耗时: {elapsed:.6f}s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

slow_sum(1_000_000)

print("\n=== 带参数的装饰器 ===")

def retry(max_attempts=3, delay=0.1):
    """带参数的装饰器 — 需要三层嵌套"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"  尝试 {attempt}/{max_attempts} 失败: {e}")
                    if attempt == max_attempts:
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

call_count = 0

@retry(max_attempts=3, delay=0.01)
def unreliable_function():
    """模拟不稳定的函数"""
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("网络错误")
    return "成功!"

result = unreliable_function()
print(f"结果: {result}")

print("\n=== 装饰器堆叠（组合）===")

def bold(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<b>{func(*args, **kwargs)}</b>"
    return wrapper

def italic(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"<i>{func(*args, **kwargs)}</i>"
    return wrapper

@bold       # 先 italic，再 bold
@italic     # 等价于: greet2 = bold(italic(greet2))
def greet2(name):
    return f"Hello, {name}"

print(f"堆叠装饰器: {greet2('World')}")

print("\n=== 类作为装饰器 ===")

class CacheDecorator:
    """用类实现装饰器（有状态的装饰器）"""

    def __init__(self, func):
        self.func = func
        self.cache = {}
        functools.update_wrapper(self, func)

    def __call__(self, *args):
        if args not in self.cache:
            self.cache[args] = self.func(*args)
        return self.cache[args]

    def clear(self):
        self.cache.clear()

@CacheDecorator
def expensive_compute(x, y):
    print(f"  计算 {x} + {y}...")
    return x + y

print(f"first call:  {expensive_compute(1, 2)}")
print(f"cached call: {expensive_compute(1, 2)}")  # 不会打印 "计算..."
print(f"缓存内容: {expensive_compute.cache}")

print("\n=== 常见内置装饰器 ===")

class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property  # 把方法变成属性访问（类似 C++ 的 getter）
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value < 0:
            raise ValueError("半径不能为负")
        self._radius = value

    @property
    def area(self):
        import math
        return math.pi * self._radius ** 2

    @staticmethod  # 类似 C++ 的 static method
    def is_valid_radius(r):
        return r >= 0

    @classmethod  # C++ 没有的概念
    def from_diameter(cls, diameter):
        return cls(diameter / 2)

c = Circle(5)
print(f"radius: {c.radius}")
print(f"area: {c.area:.2f}")
c.radius = 10
print(f"new area: {c.area:.2f}")

c2 = Circle.from_diameter(20)
print(f"from_diameter(20): radius={c2.radius}")
