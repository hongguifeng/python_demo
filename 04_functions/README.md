# 04 - 函数、闭包与装饰器

> C/C++ 的函数指针 → Python 的一等公民函数

## 核心差异

| C/C++ | Python |
|-------|--------|
| 函数不是值，需要函数指针 | 函数是对象，可以赋值、传递 |
| 固定参数列表 | `*args`, `**kwargs` 动态参数 |
| 宏/模板做代码生成 | 装饰器修改函数行为 |
| lambda（C++11）有限制 | lambda 只能单表达式但广泛使用 |
| 没有闭包（C++11 capture list） | 自然闭包 |

## 示例

```bash
python3 examples/first_class.py      # 函数作为一等公民
python3 examples/args_kwargs.py      # 灵活的参数机制
python3 examples/closures.py         # 闭包
python3 examples/decorators.py       # 装饰器模式
python3 examples/functools_demo.py   # functools 实用工具
```
