# 12 - 元编程

> C++ 的模板元编程/宏 vs Python 的 metaclass/descriptor

## 核心思想

Python 中 **类也是对象**，由**元类 (metaclass)** 创建。
这意味着你可以在运行时动态创建和修改类。

C++ 的元编程在编译时（模板），Python 的元编程在运行时。

## 示例

```bash
python3 examples/metaclass_demo.py   # 元类
python3 examples/descriptors.py      # 描述符协议
python3 examples/dynamic_class.py    # 动态类创建与修改
```
