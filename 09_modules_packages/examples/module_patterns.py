"""
模块设计模式
"""

print("=== 模式 1: 延迟导入（解决循环导入）===")

def heavy_operation():
    """只在调用时才导入（减少启动时间）"""
    import json  # 延迟导入
    return json.dumps({"status": "ok"})

print(f"延迟导入: {heavy_operation()}")

print("\n=== 模式 2: 可选依赖 ===")

try:
    import numpy as np
    HAS_NUMPY = True
except ImportError:
    HAS_NUMPY = False

if HAS_NUMPY:
    print(f"NumPy 可用: {np.__version__}")
else:
    print("NumPy 不可用 — 使用回退实现")
    # 提供纯 Python 的替代实现

print("\n=== 模式 3: 插件系统 ===")
import importlib

# 通过配置动态加载模块
plugins = {
    "json": "json",
    "path": "os.path",
}

for name, module_path in plugins.items():
    mod = importlib.import_module(module_path)
    print(f"  插件 {name}: {mod.__name__}")

print("\n=== 模式 4: 模块级别的 __getattr__（Python 3.7+）===")
# 类似 C++ 的 lazy initialization

# 在模块中可以定义:
# def __getattr__(name):
#     if name == "expensive_data":
#         import heavy_module
#         data = heavy_module.load()
#         globals()["expensive_data"] = data
#         return data
#     raise AttributeError(f"module has no attribute {name}")

print("模块级 __getattr__: 允许延迟加载模块属性")

print("\n=== 模式 5: 包的 __init__.py 作为门面 ===")
print("""
# mypackage/__init__.py
from .core import MainClass
from .utils import helper_func

__all__ = ["MainClass", "helper_func"]

# 用户只需要:
# from mypackage import MainClass
# 而不是:
# from mypackage.core import MainClass
""".strip())

print("\n=== 模式 6: 配置文件模式 ===")
# Python 模块本身就可以当配置文件

# config.py:
# DATABASE_URL = "postgres://localhost/mydb"
# DEBUG = True
# ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# 使用:
# import config
# connect(config.DATABASE_URL)

# 或者用环境变量覆盖:
import os
class Config:
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///default.db")
    DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
    PORT = int(os.environ.get("PORT", "8080"))

print(f"Config.DATABASE_URL = {Config.DATABASE_URL}")
print(f"Config.DEBUG = {Config.DEBUG}")
print(f"Config.PORT = {Config.PORT}")

print("\n=== 模式 7: if __name__ == '__main__' ===")
# Python 最重要的模式之一

def main():
    print("  这是主程序逻辑")

def add(a, b):
    return a + b

# 单元测试经常放在这里
if __name__ == "__main__":
    main()

    # 简单的自测
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    print("  所有测试通过")
