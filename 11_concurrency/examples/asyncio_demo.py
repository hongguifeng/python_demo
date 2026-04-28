"""
asyncio — Python 的异步编程框架

类比 C 的 epoll/select + 状态机，但语法优雅得多。
async/await 从生成器演化而来。
"""

import asyncio
import time

print("=== async/await 基础 ===")

async def fetch_data(name: str, delay: float) -> str:
    """模拟异步 I/O（如 HTTP 请求）"""
    print(f"  [{name}] 开始请求...")
    await asyncio.sleep(delay)  # 非阻塞等待（让出控制权）
    print(f"  [{name}] 完成 ({delay}s)")
    return f"{name}_result"

async def main_sequential():
    """顺序执行"""
    start = time.perf_counter()
    r1 = await fetch_data("A", 0.5)
    r2 = await fetch_data("B", 0.5)
    r3 = await fetch_data("C", 0.5)
    elapsed = time.perf_counter() - start
    print(f"  顺序结果: {[r1, r2, r3]}")
    print(f"  顺序耗时: {elapsed:.2f}s\n")

async def main_concurrent():
    """并发执行"""
    start = time.perf_counter()
    results = await asyncio.gather(
        fetch_data("A", 0.5),
        fetch_data("B", 0.5),
        fetch_data("C", 0.5),
    )
    elapsed = time.perf_counter() - start
    print(f"  并发结果: {results}")
    print(f"  并发耗时: {elapsed:.2f}s")

print("顺序执行:")
asyncio.run(main_sequential())

print("并发执行:")
asyncio.run(main_concurrent())

print("\n=== 异步迭代器 ===")

async def async_range(n):
    """异步生成器"""
    for i in range(n):
        await asyncio.sleep(0.01)
        yield i

async def demo_async_iter():
    print("异步 for 循环:")
    async for i in async_range(5):
        print(f"  {i}", end="")
    print()

asyncio.run(demo_async_iter())

print("\n=== 异步上下文管理器 ===")

class AsyncDatabase:
    """异步上下文管理器"""
    def __init__(self, url):
        self.url = url

    async def __aenter__(self):
        print(f"  异步连接 {self.url}")
        await asyncio.sleep(0.01)
        return self

    async def __aexit__(self, *args):
        print(f"  异步断开 {self.url}")
        await asyncio.sleep(0.01)

    async def query(self, sql):
        await asyncio.sleep(0.01)
        return f"结果: {sql}"

async def demo_async_context():
    async with AsyncDatabase("postgres://localhost") as db:
        result = await db.query("SELECT 1")
        print(f"  查询: {result}")

asyncio.run(demo_async_context())

print("\n=== Task 和取消 ===")

async def long_operation():
    try:
        print("  长操作开始...")
        await asyncio.sleep(10)
        print("  长操作完成")
    except asyncio.CancelledError:
        print("  长操作被取消!")
        raise  # 重新抛出以传播取消

async def demo_cancel():
    task = asyncio.create_task(long_operation())
    await asyncio.sleep(0.1)
    task.cancel()  # 取消任务
    try:
        await task
    except asyncio.CancelledError:
        print("  任务已取消")

asyncio.run(demo_cancel())

print("\n=== Semaphore 限流 ===")

async def limited_fetch(sem, name, delay):
    async with sem:  # 限制并发数
        print(f"  [{name}] 开始 (并发数受限)")
        await asyncio.sleep(delay)
        return name

async def demo_semaphore():
    sem = asyncio.Semaphore(2)  # 最多 2 个并发
    tasks = [limited_fetch(sem, f"req-{i}", 0.3) for i in range(5)]
    start = time.perf_counter()
    results = await asyncio.gather(*tasks)
    elapsed = time.perf_counter() - start
    print(f"  结果: {results}")
    print(f"  耗时: {elapsed:.2f}s (受限于并发数2)")

asyncio.run(demo_semaphore())

print("\n=== async 与 sync 的对比 ===")
print("""
同步 (requests):
    response = requests.get(url)
    data = response.json()

异步 (aiohttp):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()

核心原则:
  - await 只能在 async 函数中使用
  - async 函数必须用 await 调用（或 asyncio.run）
  - 不要在 async 中调用阻塞的同步函数（会阻塞事件循环）
  - 需要调用同步代码时用 asyncio.to_thread()
""".strip())
