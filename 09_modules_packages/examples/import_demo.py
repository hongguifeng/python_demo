"""
import 机制详解

C 的 #include 是文本替换（预处理器）。
Python 的 import 是执行代码并缓存模块对象。
"""

import sys

print("=== import 的几种形式 ===")

# 1. import 模块
import os
print(f"os.getcwd() = {os.getcwd()}")

# 2. from 模块 import 名称
from os.path import join, exists
print(f"join('/tmp', 'test') = {join('/tmp', 'test')}")

# 3. import as（别名）
import collections as col
print(f"Counter: {col.Counter('hello')}")

# 4. from import as
from datetime import datetime as dt
print(f"now: {dt.now().isoformat()}")

print("\n=== 模块搜索顺序 ===")
# 类似 C 的 -I include path 和 -L library path
print("sys.path (模块搜索路径):")
for i, p in enumerate(sys.path[:6]):
    print(f"  [{i}] {p}")
if len(sys.path) > 6:
    print(f"  ... 共 {len(sys.path)} 个路径")

# 搜索顺序:
# 1. 当前目录（或脚本所在目录）
# 2. PYTHONPATH 环境变量
# 3. 标准库
# 4. site-packages（第三方库）

print("\n=== 模块是对象 ===")
import json
print(f"json 模块:")
print(f"  类型:  {type(json)}")
print(f"  文件:  {json.__file__}")
print(f"  名称:  {json.__name__}")
print(f"  包:    {json.__package__}")

print("\n=== 模块只导入一次 ===")
# 类似 C 的 #pragma once，但更强大
# 第二次 import 直接返回缓存的模块对象

print(f"json 在 sys.modules 中: {'json' in sys.modules}")
json_1 = __import__('json')
json_2 = __import__('json')
print(f"同一个对象: {json_1 is json_2}")

print("\n=== __name__ 和 __main__ ===")
# C 的入口点是 main()
# Python 的入口点是 __name__ == "__main__" 的模块

print(f"当前模块的 __name__ = {__name__!r}")

# 标准模式：
# if __name__ == "__main__":
#     main()
# 这让文件既可以作为脚本运行，也可以被导入

print("\n=== 包结构 ===")
print("""
mypackage/                  # 包目录
├── __init__.py             # 包的初始化代码（import mypackage 时执行）
├── __main__.py             # python -m mypackage 时执行
├── core.py                 # 子模块
├── utils.py                # 子模块
└── subpackage/             # 子包
    ├── __init__.py
    └── helpers.py

导入方式:
  import mypackage                    # 执行 __init__.py
  from mypackage import core          # 导入子模块
  from mypackage.core import MyClass  # 导入具体名称
  from mypackage.subpackage import helpers
""".strip())

print("\n=== __all__ 控制导出 ===")
# 类似 C++ 的 public/private 但只影响 from module import *

# 在模块中定义:
# __all__ = ["public_func", "PublicClass"]  # 只有这些被 * 导出
# _private_func = ...  # 约定: 下划线前缀不被 * 导出

# 示例：查看 os 模块导出了什么
import os
print(f"os.__all__ 中的前 10 个: {os.__all__[:10]}")

print("\n=== 动态导入 ===")
# 运行时决定导入什么（C 中需要 dlopen/LoadLibrary）
import importlib

# 按名称导入模块
mod = importlib.import_module("json")
print(f"动态导入 json: {mod.dumps([1, 2, 3])}")

# 重新加载模块（开发时有用）
# importlib.reload(mod)

print("\n=== 常见陷阱 ===")

# 1. 循环导入
# a.py: from b import func_b
# b.py: from a import func_a
# 解决：延迟导入（在函数内部 import）或重构

# 2. 相对导入
# from . import sibling      # 同级模块
# from .. import parent      # 上级包
# from .sibling import func  # 同级模块中的名称
# 注意：相对导入只能在包内使用，不能在脚本中使用

# 3. 不要用通配符导入
# from module import *  # 污染命名空间，不清楚导入了什么
print("避免: from module import * (除了在 __init__.py 中收集子模块)")
