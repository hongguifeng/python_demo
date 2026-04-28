# 09 - 模块与包系统

> C/C++ 的 `#include` / 链接 vs Python 的 `import`

## 核心差异

| C/C++ | Python |
|-------|--------|
| `#include` 文本替换 | `import` 执行模块代码 |
| 头文件 + 实现文件 | 单个 `.py` 文件 |
| 编译时链接 | 运行时导入 |
| `#pragma once` / include guard | 模块只导入一次（自动缓存） |
| 静态库/动态库 | 包 (package) |
| `CMakeLists.txt` 配置路径 | `sys.path` 搜索路径 |

## 关键概念

- **模块 (module)**：一个 `.py` 文件
- **包 (package)**：包含 `__init__.py` 的目录
- **命名空间包 (namespace package)**：不需要 `__init__.py` (PEP 420)

## 示例

```bash
python3 examples/import_demo.py       # import 机制
python3 examples/module_patterns.py   # 模块设计模式
```
