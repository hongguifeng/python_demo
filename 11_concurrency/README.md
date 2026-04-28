# 11 - 并发与并行编程

> C/C++ 的 pthread/std::thread vs Python 的 GIL/threading/asyncio

## 核心差异

| C/C++ | Python |
|-------|--------|
| 真正的多线程并行 | GIL 限制 CPU 并行 |
| `pthread` / `std::thread` | `threading` 模块 |
| `fork()` | `multiprocessing` 模块 |
| `epoll` / `select` | `asyncio`（协程） |
| 手动同步 (mutex) | 同样需要同步原语 |

## GIL (Global Interpreter Lock)

**这是 C/C++ 开发者必须理解的最重要概念。**

CPython 有全局解释器锁 (GIL)：同一时刻只有一个线程可以执行 Python 字节码。

- **CPU 密集型任务**：多线程无法并行 → 用 `multiprocessing`
- **I/O 密集型任务**：GIL 在 I/O 时释放 → 多线程有效
- **异步 I/O**：`asyncio` 单线程协程 → 最佳 I/O 并发

> Python 3.13+ 实验性支持 free-threaded (no-GIL) 模式

## 示例

```bash
python3 examples/threading_demo.py      # 多线程
python3 examples/multiprocessing_demo.py # 多进程
python3 examples/asyncio_demo.py        # 异步编程
python3 examples/concurrent_demo.py     # concurrent.futures
```
