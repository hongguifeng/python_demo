"""
上下文管理器 — Python 的 RAII 替代方案

C++ 的 RAII：构造函数获取资源，析构函数释放资源
Python 的 with：__enter__ 获取资源，__exit__ 释放资源

关键区别：Python 的 with 是显式的，C++ 的 RAII 是隐式的
"""

import time
import os
import tempfile

print("=== 基本 with 语句 ===")

# 文件操作（最常见的用法）
# C:     FILE* f = fopen("test.txt", "w"); ... fclose(f);
# C++:   { std::ofstream f("test.txt"); ... }  // RAII
# Python:
tmpfile = tempfile.mktemp(suffix=".txt")
with open(tmpfile, 'w') as f:
    f.write("Hello, World!")
    # 无论是否异常，文件都会被正确关闭
# f 已关闭
print(f"文件已关闭: {f.closed}")

# 读回来
with open(tmpfile) as f:
    print(f"内容: {f.read()}")
os.unlink(tmpfile)

print("\n=== 自定义上下文管理器（类实现）===")

class DatabaseConnection:
    """模拟数据库连接 — 类似 C++ 的 RAII 封装"""

    def __init__(self, url):
        self.url = url
        self.connected = False

    def __enter__(self):
        """获取资源"""
        print(f"  连接到 {self.url}")
        self.connected = True
        return self  # 返回值绑定到 as 变量

    def __exit__(self, exc_type, exc_val, exc_tb):
        """释放资源（保证调用，即使有异常）"""
        print(f"  断开 {self.url}")
        self.connected = False
        # 返回 True 会抑制异常（通常返回 False/None）
        return False

with DatabaseConnection("postgres://localhost/mydb") as db:
    print(f"  连接状态: {db.connected}")
    # 做数据库操作...
print(f"连接状态: {db.connected}")

# 即使有异常也能正确清理
print("\n异常情况:")
try:
    with DatabaseConnection("postgres://localhost/mydb") as db:
        raise RuntimeError("查询失败")
except RuntimeError as e:
    print(f"  捕获: {e}")

print("\n=== 多个上下文管理器 ===")

# 嵌套 with
# with open("in.txt") as fin:
#     with open("out.txt", "w") as fout:
#         fout.write(fin.read())

# Python 3.10+ 支持圆括号分组
# with (
#     open("in.txt") as fin,
#     open("out.txt", "w") as fout,
# ):
#     fout.write(fin.read())

print("\n=== contextlib 工具 ===")
from contextlib import contextmanager, suppress, redirect_stdout
import io

# @contextmanager — 用生成器实现上下文管理器
@contextmanager
def timer(label):
    start = time.perf_counter()
    try:
        yield  # 执行 with 块
    finally:
        elapsed = time.perf_counter() - start
        print(f"  [{label}] {elapsed:.6f}s")

with timer("求和"):
    total = sum(range(1_000_000))
    print(f"  总和: {total}")

# suppress — 抑制特定异常
print("\nsuppress:")
with suppress(FileNotFoundError):
    os.remove("/tmp/nonexistent_file_12345.txt")
    print("  这行不会执行")
print("  继续执行（异常被抑制）")

# redirect_stdout — 重定向输出
print("\nredirect_stdout:")
buffer = io.StringIO()
with redirect_stdout(buffer):
    print("这会写入 buffer 而非终端")
    print("第二行")
print(f"  捕获的输出: {buffer.getvalue()!r}")

print("\n=== 上下文管理器 vs RAII ===")
print("""
相同点:
  - 都保证资源清理
  - 都能处理异常

不同点:
  - RAII 是隐式的（作用域结束自动调用）
  - with 是显式的（必须在 with 块中）
  - RAII 绑定到对象生命周期
  - with 绑定到代码块

  C++:
    {
        std::lock_guard<std::mutex> lock(mtx);
        // 自动释放
    }

  Python:
    with lock:
        # 自动释放
        pass

  Python 没有隐式 RAII，因为 __del__ 调用时机不确定。
  所以需要 with 来保证确定性清理。
""".strip())
