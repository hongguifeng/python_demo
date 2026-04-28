# 10 - 类型提示与静态分析

> C++ 的静态类型 vs Python 的渐进式类型 (Gradual Typing)

## 核心思想

Python 3.5 引入类型提示 (Type Hints)，允许**可选地**给代码添加类型注解。
它不影响运行时行为，但允许工具（mypy、Pyright）在运行前发现错误。

| C++ | Python 类型提示 |
|-----|----------------|
| 编译器强制检查 | 工具检查（可选） |
| 必须声明类型 | 可以逐步添加 |
| 模板/概念实现泛型 | `TypeVar`/`Generic` |
| `const` | `Final` |
| 接口（纯虚类） | `Protocol`（结构化子类型） |

## 示例

```bash
python3 examples/type_hints_basics.py  # 类型提示基础
python3 examples/advanced_types.py     # 高级类型特性
```
