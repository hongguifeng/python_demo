# 03 - 数据模型与内置类型

> C/C++ 的 array/struct vs Python 的 list/dict/tuple

## 核心对比

| C/C++ | Python | 区别 |
|-------|--------|------|
| `int[]` / `std::array` | `list` | Python list 可存不同类型，动态大小 |
| `struct` | `dict` / `dataclass` | dict 是哈希表，key-value |
| `std::pair` / 多返回值 | `tuple` | 不可变序列 |
| `std::set` | `set` | 类似 |
| `enum` | `enum.Enum` | Python 的更灵活 |
| `const` | tuple / frozenset | 不可变集合 |

## 可变 vs 不可变

这是 Python 最重要的概念之一：

| 不可变 (Immutable) | 可变 (Mutable) |
|-------------------|----------------|
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |
| `bytes` | 自定义类（默认） |

**不可变对象可以作为 dict 的 key 和 set 的元素**（因为 hash 值不变）。

## 示例

```bash
python3 examples/list_vs_array.py    # list 详解
python3 examples/dict_deep.py        # dict 详解
python3 examples/tuple_set.py        # tuple 和 set
python3 examples/comprehensions.py   # 推导式 — Python 最强特性之一
python3 examples/slicing.py          # 切片操作
```
