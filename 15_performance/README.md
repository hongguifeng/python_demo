# 15 - 性能分析与优化

> C/C++ 的 valgrind/perf vs Python 的 cProfile/timeit

## Python 性能的现实

Python 通常比 C 慢 10-100x。但这不意味着 Python 程序就慢：

1. **I/O 密集型**程序瓶颈不在 CPU（Python 够用）
2. **热点代码**可以用 C 扩展加速（NumPy 就是这样）
3. **算法复杂度**比语言速度更重要（O(n) Python > O(n²) C）
4. **开发效率**经常比运行效率更重要

## 优化原则

> "Premature optimization is the root of all evil" — Donald Knuth

1. 先让代码正确
2. 再测量找出瓶颈
3. 只优化瓶颈

## 示例

```bash
python3 examples/profiling.py      # 性能分析工具
python3 examples/optimization.py   # 优化技巧
```
