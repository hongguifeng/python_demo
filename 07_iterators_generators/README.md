# 07 - 迭代器与生成器

> C++ 的 iterator 模式 vs Python 的 yield 魔法

## 核心差异

| C++ | Python |
|-----|--------|
| `begin()/end()` + `++/*/!=` | `__iter__()/__next__()` |
| iterator 是模板+编译时 | iterator 是协议+运行时 |
| 没有 yield | **生成器** — 惰性计算的核心 |
| ranges (C++20) | 生成器表达式 + itertools |

## 为什么重要

生成器是 Python 最独特的特性之一，可以：
- 处理无限序列
- 节省内存（惰性计算）
- 简化状态机
- 构建数据管道
- 实现协程

## 示例

```bash
python3 examples/iterator_protocol.py  # 迭代器协议
python3 examples/generators.py         # 生成器基础
python3 examples/generator_advanced.py # 生成器高级用法
python3 examples/itertools_demo.py     # itertools 工具箱
```
