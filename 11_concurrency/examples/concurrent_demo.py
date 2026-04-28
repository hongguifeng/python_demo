"""
concurrent.futures — 高层并发接口

统一的接口同时支持线程池和进程池，
类似 Java 的 ExecutorService / C++ 的 std::async。
"""

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import time

def download(url):
    """模拟下载"""
    time.sleep(0.3)
    return f"内容 from {url}"

def cpu_work(n):
    """CPU 密集型"""
    return sum(i * i for i in range(n))

print("=== ThreadPoolExecutor — I/O 并发 ===")

urls = [f"https://example.com/page/{i}" for i in range(6)]

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=3) as executor:
    # map: 并行 map（保持顺序）
    results = list(executor.map(download, urls))
elapsed = time.perf_counter() - start

print(f"下载 {len(urls)} 页:")
for r in results[:3]:
    print(f"  {r}")
print(f"  ... 共 {len(results)} 个结果")
print(f"  耗时: {elapsed:.2f}s (3 线程并发)")

print("\n=== Future 对象 ===")

with ThreadPoolExecutor(max_workers=2) as executor:
    # submit: 提交单个任务，返回 Future
    future = executor.submit(download, "https://example.com")
    print(f"Future 状态: running={future.running()}")

    # 获取结果（阻塞）
    result = future.result(timeout=5)
    print(f"Future 结果: {result}")
    print(f"Future 完成: {future.done()}")

print("\n=== as_completed — 按完成顺序获取 ===")
from concurrent.futures import as_completed

def variable_work(name, seconds):
    time.sleep(seconds)
    return f"{name} (耗时 {seconds}s)"

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(variable_work, "快任务", 0.1): "快",
        executor.submit(variable_work, "中任务", 0.3): "中",
        executor.submit(variable_work, "慢任务", 0.5): "慢",
    }

    print("按完成顺序:")
    for future in as_completed(futures):
        label = futures[future]
        print(f"  [{label}] {future.result()}")

print("\n=== ProcessPoolExecutor — CPU 并行 ===")

if __name__ == "__main__":
    N = 2_000_000

    # 单进程
    start = time.perf_counter()
    results_single = [cpu_work(N) for _ in range(4)]
    single_time = time.perf_counter() - start

    # 多进程
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as executor:
        results_multi = list(executor.map(cpu_work, [N] * 4))
    multi_time = time.perf_counter() - start

    print(f"CPU 密集型 (4次):")
    print(f"  单进程: {single_time:.3f}s")
    print(f"  多进程: {multi_time:.3f}s")
    print(f"  加速比: {single_time/multi_time:.1f}x")

    print("\n=== 错误处理 ===")

    def might_fail(x):
        if x == 3:
            raise ValueError(f"不能处理 {x}")
        return x ** 2

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(might_fail, i) for i in range(5)]
        for i, future in enumerate(futures):
            try:
                result = future.result()
                print(f"  任务 {i}: {result}")
            except ValueError as e:
                print(f"  任务 {i}: 错误 - {e}")

    print("\n=== 选择指南 ===")
    print("""
    ThreadPoolExecutor:
      ✓ I/O 密集型（网络、文件、数据库）
      ✓ 轻量（共享内存）
      ✓ 简单（和主进程共享对象）

    ProcessPoolExecutor:
      ✓ CPU 密集型（计算、数据处理）
      ✓ 绕过 GIL
      ✗ 序列化开销（进程间传递数据要 pickle）
      ✗ 内存开销大

    asyncio:
      ✓ 超高并发 I/O（数万连接）
      ✓ 无锁编程（单线程）
      ✗ 需要异步库支持
    """.strip())
