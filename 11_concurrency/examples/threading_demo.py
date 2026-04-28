"""
多线程 — threading 模块

Python 的线程和 C 的 pthread 类似，但受 GIL 限制。
"""

import threading
import time

print("=== 基本线程 ===")

def worker(name, seconds):
    """工作线程函数"""
    print(f"  [{name}] 开始工作")
    time.sleep(seconds)  # I/O 模拟：GIL 在 sleep 时释放
    print(f"  [{name}] 完成 ({seconds}s)")
    return name

# 创建线程（类似 pthread_create）
threads = []
start = time.perf_counter()

for i in range(3):
    t = threading.Thread(target=worker, args=(f"Thread-{i}", 0.5))
    threads.append(t)
    t.start()  # 启动线程

# 等待所有线程完成（类似 pthread_join）
for t in threads:
    t.join()

elapsed = time.perf_counter() - start
print(f"总耗时: {elapsed:.2f}s (3个线程并行)")

print("\n=== GIL 对 CPU 密集型的影响 ===")

def cpu_work(n):
    """CPU 密集型任务"""
    total = 0
    for i in range(n):
        total += i * i
    return total

N = 5_000_000

# 单线程
start = time.perf_counter()
cpu_work(N)
cpu_work(N)
single_time = time.perf_counter() - start

# 多线程
start = time.perf_counter()
t1 = threading.Thread(target=cpu_work, args=(N,))
t2 = threading.Thread(target=cpu_work, args=(N,))
t1.start()
t2.start()
t1.join()
t2.join()
multi_time = time.perf_counter() - start

print(f"CPU 密集型任务 (2次):")
print(f"  单线程: {single_time:.3f}s")
print(f"  多线程: {multi_time:.3f}s")
print(f"  多线程{'更慢' if multi_time >= single_time else '更快'}")
print(f"  (GIL 导致 CPU 密集型多线程没有加速效果)")

print("\n=== 线程同步 ===")
# 和 C 的 mutex 几乎一样

counter = 0
lock = threading.Lock()

def increment_unsafe():
    global counter
    for _ in range(100_000):
        counter += 1  # 不是原子操作！

def increment_safe():
    global counter
    for _ in range(100_000):
        with lock:  # 自动 acquire/release
            counter += 1

# 不安全版本
counter = 0
threads = [threading.Thread(target=increment_unsafe) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"不安全计数 (期望 200000): {counter}")

# 安全版本
counter = 0
threads = [threading.Thread(target=increment_safe) for _ in range(2)]
for t in threads:
    t.start()
for t in threads:
    t.join()
print(f"安全计数 (期望 200000): {counter}")

print("\n=== 线程本地存储 ===")
# 类似 C 的 thread_local / __thread

local_data = threading.local()

def show_local(name):
    local_data.name = name  # 每个线程有自己的 name
    time.sleep(0.01)
    print(f"  Thread {threading.current_thread().name}: local_data.name = {local_data.name}")

threads = [threading.Thread(target=show_local, args=(f"worker_{i}",), name=f"T-{i}")
           for i in range(3)]
for t in threads:
    t.start()
for t in threads:
    t.join()

print("\n=== 其他同步原语 ===")
# threading.Event — 事件通知
event = threading.Event()

def waiter():
    print("  等待事件...")
    event.wait()
    print("  事件触发!")

t = threading.Thread(target=waiter)
t.start()
time.sleep(0.1)
event.set()  # 触发事件
t.join()

# threading.Semaphore — 信号量
# threading.Condition — 条件变量
# threading.Barrier — 屏障
print("\n其他: Semaphore, Condition, Barrier（和 POSIX 线程一样）")
