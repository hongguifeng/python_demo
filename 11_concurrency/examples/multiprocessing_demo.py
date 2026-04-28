"""
多进程 — 绕过 GIL 实现真正的并行

multiprocessing 模块创建独立进程（类似 fork）。
每个进程有自己的 Python 解释器和 GIL。
"""

import multiprocessing as mp
import time
import os

def cpu_work(n):
    """CPU 密集型任务"""
    total = 0
    for i in range(n):
        total += i * i
    return total

def worker_info(name):
    """显示进程信息"""
    print(f"  [{name}] PID={os.getpid()}, Parent={os.getppid()}")
    return name

if __name__ == "__main__":
    print("=== 基本多进程 ===")

    # 显示进程信息
    print(f"主进程 PID: {os.getpid()}")

    processes = []
    for i in range(3):
        p = mp.Process(target=worker_info, args=(f"Worker-{i}",))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    print("\n=== CPU 密集型：多进程 vs 多线程 ===")
    N = 5_000_000

    # 单进程
    start = time.perf_counter()
    cpu_work(N)
    cpu_work(N)
    single_time = time.perf_counter() - start

    # 多进程
    start = time.perf_counter()
    p1 = mp.Process(target=cpu_work, args=(N,))
    p2 = mp.Process(target=cpu_work, args=(N,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    multi_time = time.perf_counter() - start

    print(f"CPU 密集型 (2次):")
    print(f"  单进程: {single_time:.3f}s")
    print(f"  多进程: {multi_time:.3f}s")
    cpu_count = mp.cpu_count()
    print(f"  CPU 核心数: {cpu_count}")

    print("\n=== Pool — 进程池 ===")
    # 类似线程池，但用进程

    with mp.Pool(processes=4) as pool:
        # map: 并行 map
        results = pool.map(cpu_work, [1_000_000] * 4)
        print(f"Pool.map 结果数量: {len(results)}")

        # apply_async: 异步提交单个任务
        future = pool.apply_async(cpu_work, (1_000_000,))
        print(f"apply_async 结果: {future.get(timeout=10)}")

    print("\n=== 进程间通信 ===")

    # Queue（和 C 的消息队列类似）
    def producer(queue, items):
        for item in items:
            queue.put(item)
        queue.put(None)  # 毒丸信号

    def consumer(queue):
        results = []
        while True:
            item = queue.get()
            if item is None:
                break
            results.append(item * 2)
        return results

    q = mp.Queue()
    p = mp.Process(target=producer, args=(q, [1, 2, 3, 4, 5]))
    p.start()

    results = consumer(q)  # 主进程消费
    p.join()
    print(f"Queue 通信结果: {results}")

    # 共享内存（类似 mmap）
    print("\n=== 共享内存 ===")
    shared_val = mp.Value('i', 0)  # 'i' = int
    shared_arr = mp.Array('d', [0.0, 0.0, 0.0])  # 'd' = double

    def modify_shared(val, arr):
        val.value = 42
        for i in range(len(arr)):
            arr[i] = float(i * 10)

    p = mp.Process(target=modify_shared, args=(shared_val, shared_arr))
    p.start()
    p.join()

    print(f"共享值: {shared_val.value}")
    print(f"共享数组: {list(shared_arr)}")

    print("\n=== 何时用多进程 vs 多线程 ===")
    print("""
    多线程 (threading):
      ✓ I/O 密集型（网络请求、文件读写）
      ✓ 共享内存简单
      ✗ CPU 密集型无法并行（GIL）

    多进程 (multiprocessing):
      ✓ CPU 密集型（计算、数据处理）
      ✓ 真正的并行
      ✗ 进程间通信复杂
      ✗ 内存开销大（每个进程独立地址空间）

    asyncio:
      ✓ 大量 I/O 并发（数千连接）
      ✓ 单线程，无竞争条件
      ✗ CPU 密集型不适用
    """.strip())
