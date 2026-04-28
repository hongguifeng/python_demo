# 06 - 内存管理与对象生命周期

> C++ 的 malloc/RAII/智能指针 vs Python 的引用计数/GC

## 核心差异

| C/C++ | Python (CPython) |
|-------|-----------------|
| 手动 malloc/free | 自动引用计数 + GC |
| 栈分配 vs 堆分配 | 一切都在堆上（对象） |
| RAII 确定性析构 | `__del__` 不保证调用时机 |
| `shared_ptr`/`unique_ptr` | 天然引用计数 |
| 值语义 vs 引用语义 | 一切都是引用语义 |

## 示例

```bash
python3 examples/refcount.py          # 引用计数机制
python3 examples/gc_demo.py           # 垃圾回收
python3 examples/memory_pitfalls.py   # 内存陷阱
```
