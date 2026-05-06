"""
展示 Python 运行环境的详细信息

对 C/C++ 开发者来说，这相当于查看编译器和系统配置。
"""

import sys
import os
import platform
import struct

print("=" * 60)
print("Python 运行环境信息")
print("=" * 60)

print(f"\n--- 解释器信息 ---")
print(f"  版本:       {sys.version}")
print(f"  实现:       {sys.implementation.name} {sys.implementation.version.major}.{sys.implementation.version.minor}")
print(f"  编译器:     {platform.python_compiler()}")
print(f"  可执行文件: {sys.executable}")

print(f"\n--- 平台信息 ---")
print(f"  操作系统:   {platform.system()} {platform.release()}")
print(f"  架构:       {platform.machine()}")
print(f"  指针大小:   {struct.calcsize('P') * 8} 位")  # 类似 sizeof(void*)
print(f"  字节序:     {sys.byteorder}")

print(f"\n--- 路径信息 ---")
print(f"  模块搜索路径 (类似 -I include path):")
for p in sys.path:
    print(f"    {p}")

print(f"\n--- 资源限制 ---")
print(f"  最大递归深度:     {sys.getrecursionlimit()}")
print(f"  整数最大长度:     无限制")
print(f"  浮点数信息:       max={sys.float_info.max:.2e}, epsilon={sys.float_info.epsilon}")

print(f"\n--- 虚拟环境检测 ---")
venv = os.environ.get('VIRTUAL_ENV')
if venv:
    print(f"  当前虚拟环境: {venv}")
else:
    print(f"  未在虚拟环境中运行")
    print(f"  (建议: python3 -m venv myenv && source myenv/bin/activate)")

# 对比 C/C++：Python 对象的内存开销
print(f"\n--- 对象内存开销 (C/C++ 开发者关注) ---")
print(f"  int 对象大小:     {sys.getsizeof(0)} bytes  (C 中 int 只需 4 bytes)")
print(f"  float 对象大小:   {sys.getsizeof(0.0)} bytes (C 中 double 只需 8 bytes)")
print(f"  空 str 大小:      {sys.getsizeof('')} bytes")
print(f"  空 list 大小:     {sys.getsizeof([])} bytes  (C 中空数组 0 bytes)")
print(f"  空 dict 大小:     {sys.getsizeof({})} bytes")
print(f"  注意：Python 的每个对象都有引用计数和类型指针的开销")
