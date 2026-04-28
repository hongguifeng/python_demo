# 05 - 面向对象与鸭子类型

> C++ 的 vtable/虚函数 vs Python 的 duck typing / MRO

## 核心差异

| C++ | Python |
|-----|--------|
| 编译时类型检查 | 运行时鸭子类型 |
| 虚函数表 (vtable) 实现多态 | 方法解析顺序 (MRO) |
| public/protected/private | 约定 `_private` / `__mangled` |
| 单继承 + 接口 | 多重继承 |
| 头文件声明 + 实现分离 | 一切在 class 块中 |
| 构造/析构确定性 | `__init__`/`__del__` |
| 运算符重载 | 魔术方法 (`__add__`, `__eq__` 等) |
| 模板（编译时泛型） | 天然泛型（动态类型） |

## 示例

```bash
python3 examples/class_basics.py    # 类基础与对比
python3 examples/dunder.py          # 魔术方法
python3 examples/inheritance.py     # 继承与 MRO
python3 examples/duck_typing.py     # 鸭子类型
python3 examples/dataclasses_demo.py # dataclass — 现代 Python 的 struct
```
