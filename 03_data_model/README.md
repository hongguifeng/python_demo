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

## 3.1 推导式语法

推导式的本质是：**用一行表达式描述“从可迭代对象中取值、可选过滤、再生成新容器”**。

最常见的 4 种形式：

```python
# 列表推导式
[expr for item in iterable if condition]

# 字典推导式
{key_expr: value_expr for item in iterable if condition}

# 集合推导式
{expr for item in iterable if condition}

# 生成器表达式
(expr for item in iterable if condition)
```

可以这样读：

- `expr` / `key_expr` / `value_expr`：最终要放进结果里的表达式
- `for item in iterable`：数据来源
- `if condition`：可选过滤条件，不满足就跳过

例如：

```python
[x * x for x in range(10) if x % 2 == 0]
```

含义是：从 `range(10)` 里依次取出 `x`，只保留偶数，并把 `x * x` 放进结果列表。

### 嵌套推导式怎么读

```python
[(x, y) for x in range(3) for y in range(3) if x != y]
```

它等价于：

```python
result = []
for x in range(3):
	for y in range(3):
		if x != y:
			result.append((x, y))
```

规则很简单：**推导式里 `for` 和 `if` 的顺序，和你把它展开成普通循环后的顺序一致。**

### 什么时候用

- 结果是“从一个序列变换得到另一个序列”时，用推导式通常最清晰
- 逻辑只有一层变换加一层过滤时，推导式通常优于普通循环
- 如果嵌套太深、条件太复杂，宁可改回普通 `for` 循环，避免可读性下降

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
