"""
闭包 (Closures)

C 没有闭包。C++11 的 lambda capture 类似但更受限。
Python 的闭包是自然的。
"""

print("=== 基本闭包 ===")

def make_counter(start=0):
    """创建一个计数器 — 类似 C++ 的有状态仿函数"""
    count = start

    def increment():
        nonlocal count
        count += 1
        return count

    def get():
        return count

    def reset():
        nonlocal count
        count = start

    # 返回多个闭包，它们共享同一个 count
    return increment, get, reset

inc, get, reset = make_counter(10)
print(f"初始: {get()}")
print(f"inc: {inc()}, {inc()}, {inc()}")
print(f"当前: {get()}")
reset()
print(f"重置后: {get()}")

print("\n=== 闭包捕获的是变量，不是值！===")
# 这是最常见的闭包陷阱，C++ lambda 的 [=] 按值捕获不会有这个问题

def make_functions_wrong():
    """错误示例：所有函数共享同一个 i"""
    funcs = []
    for i in range(5):
        funcs.append(lambda: i)  # 捕获的是变量 i，不是 i 的值
    return funcs

funcs = make_functions_wrong()
print("错误的闭包:")
for f in funcs:
    print(f"  f() = {f()}")  # 全是 4！因为循环结束后 i=4

def make_functions_right():
    """正确：用默认参数捕获当前值"""
    funcs = []
    for i in range(5):
        funcs.append(lambda x=i: x)  # 默认参数在定义时求值
    return funcs

funcs = make_functions_right()
print("\n正确的闭包:")
for f in funcs:
    print(f"  f() = {f()}")

print("\n=== 闭包的实际应用 ===")

# 1. 缓存/记忆化
def memoize(func):
    """手动实现记忆化（functools.lru_cache 更好）"""
    cache = {}

    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]

    wrapper.cache = cache  # 暴露缓存以便调试
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"fib(30) = {fibonacci(30)}")
print(f"缓存命中: {len(fibonacci.cache)} 个条目")

# 2. 配置工厂
def make_logger(prefix, level="INFO"):
    """创建带配置的日志函数"""
    def log(message):
        print(f"[{level}] {prefix}: {message}")
    return log

db_log = make_logger("Database", "DEBUG")
api_log = make_logger("API")

db_log("Connected")
api_log("Request received")

print("\n=== 闭包内部机制 ===")
def outer(x):
    def inner(y):
        return x + y
    return inner

add5 = outer(5)

# 查看闭包捕获的变量
print(f"闭包变量: {add5.__closure__}")
print(f"捕获的值: {add5.__closure__[0].cell_contents}")
print(f"自由变量: {add5.__code__.co_freevars}")
print(f"add5(3) = {add5(3)}")
