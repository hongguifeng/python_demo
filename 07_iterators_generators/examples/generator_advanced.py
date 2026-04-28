"""
生成器高级用法 — 协程、状态机、上下文管理器
"""

print("=== 生成器作为协程（简单版）===")
# Python 的 async/await 就是从生成器演化来的

def coroutine(func):
    """自动启动协程的装饰器"""
    def wrapper(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)  # 自动 prime
        return gen
    return wrapper

@coroutine
def averager():
    """运行中的平均值计算器"""
    total = 0.0
    count = 0
    average = None
    while True:
        value = yield average
        total += value
        count += 1
        average = total / count

avg = averager()
for v in [10, 20, 30, 40, 50]:
    result = avg.send(v)
    print(f"  send({v}): 平均值 = {result}")

print("\n=== 生成器实现状态机 ===")

def traffic_light():
    """交通灯状态机"""
    while True:
        # 绿灯
        for _ in range(3):  # 绿灯 3 个周期
            yield "🟢 GREEN"
        # 黄灯
        yield "🟡 YELLOW"
        # 红灯
        for _ in range(2):  # 红灯 2 个周期
            yield "🔴 RED"

light = traffic_light()
for i in range(10):
    print(f"  周期 {i}: {next(light)}")

print("\n=== 生成器实现上下文管理器 ===")
from contextlib import contextmanager
import time

@contextmanager
def timer(label=""):
    """用生成器实现上下文管理器 — 不需要类"""
    start = time.perf_counter()
    yield  # yield 之前 = __enter__，yield 之后 = __exit__
    elapsed = time.perf_counter() - start
    print(f"  [{label}] 耗时: {elapsed:.6f}s")

with timer("计算"):
    total = sum(range(1_000_000))
    print(f"  结果: {total}")

@contextmanager
def temporary_value(obj, attr, value):
    """临时修改属性（类似 C++ 的 RAII guard）"""
    old_value = getattr(obj, attr)
    setattr(obj, attr, value)
    try:
        yield
    finally:
        setattr(obj, attr, old_value)

class Config:
    debug = False

config = Config()
print(f"\n修改前: debug={config.debug}")
with temporary_value(config, 'debug', True):
    print(f"修改中: debug={config.debug}")
print(f"修改后: debug={config.debug}")

print("\n=== 生成器的 close() 和 throw() ===")

def managed_resource():
    """生成器中的资源管理"""
    print("  获取资源")
    try:
        while True:
            yield "data"
    except GeneratorExit:
        print("  释放资源 (GeneratorExit)")
    except Exception as e:
        print(f"  处理异常: {e}")
        yield "error_handled"

gen = managed_resource()
print(f"  next: {next(gen)}")
gen.close()  # 触发 GeneratorExit

print()
gen = managed_resource()
print(f"  next: {next(gen)}")
result = gen.throw(ValueError, "测试错误")  # 向生成器抛异常
print(f"  throw result: {result}")

print("\n=== 实际应用：分块读取 ===")

def chunked(iterable, size):
    """将可迭代对象分成固定大小的块
    实际应用：分批处理数据库记录、分块上传等"""
    chunk = []
    for item in iterable:
        chunk.append(item)
        if len(chunk) == size:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

data = list(range(17))
print(f"原始: {data}")
print(f"分块(5):")
for chunk in chunked(data, 5):
    print(f"  {chunk}")
