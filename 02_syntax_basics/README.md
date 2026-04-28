# 02 - 语法差异速览

> C/C++ 开发者最常踩的坑和最需要转变的思维

## 核心思维转变

**C/C++：你在操作内存中的数据**
**Python：你在操作对象的引用（名字绑定到对象）**

这个区别贯穿 Python 的一切设计。

## 2.1 变量不是"盒子"，而是"标签"

在 C 中，变量是一块内存：
```c
int x = 42;    // x 是一个 4 字节的内存位置，里面存着 42
int y = x;     // y 是另一块 4 字节内存，值被复制过去
x = 100;       // 修改 x 的内存，y 不受影响
```

在 Python 中，变量是"名字"，贴在对象上：
```python
x = 42          # 创建 int 对象 42，名字 x 指向它
y = x           # 名字 y 也指向同一个对象 42
x = 100         # x 指向新对象 100，y 仍然指向 42
```

```bash
python3 examples/name_binding.py
```

## 2.2 动态类型

```c
int x = 42;
x = "hello";   // 编译错误！
```

```python
x = 42          # x 绑定到 int
x = "hello"     # x 重新绑定到 str，完全合法
x = [1, 2, 3]  # x 又绑定到 list
```

类型属于**对象**而非**变量**。变量只是名字。

```bash
python3 examples/dynamic_typing.py
```

## 2.3 缩进即作用域

C/C++ 用 `{}`，Python 用缩进（通常 4 个空格）：

```c
if (x > 0) {
    printf("positive\n");
    if (x > 100) {
        printf("large\n");
    }
}
```

```python
if x > 0:
    print("positive")
    if x > 100:
        print("large")
```

**注意**：混用 tab 和空格会报错。统一用 4 空格。

## 2.4 没有声明，只有赋值

```c
int x;          // 声明
x = 42;         // 赋值
int y = 10;     // 声明 + 初始化
```

```python
# 没有"声明"这个概念
x = 42          # 第一次赋值即创建
# 使用未赋值的变量会抛出 NameError
```

## 2.5 真值判断

C/C++ 中 0 为假，非 0 为真。Python 更丰富：

| 假值 (Falsy) | 真值 (Truthy) |
|---------------|---------------|
| `None` | 其他一切 |
| `False` | `True` |
| `0`, `0.0`, `0j` | 非零数字 |
| `""` (空字符串) | 非空字符串 |
| `[]`, `()`, `{}`, `set()` | 非空容器 |

```bash
python3 examples/truthiness.py
```

## 2.6 多重赋值与解包

C++ 17 有结构化绑定，但 Python 的解包更灵活：

```bash
python3 examples/unpacking.py
```

## 2.7 字符串

C/C++ 的字符串是 `char` 数组/`std::string`。Python 字符串是不可变的 Unicode 对象：

```bash
python3 examples/strings.py
```

## 2.8 运算符差异

```bash
python3 examples/operators.py
```

## 2.9 作用域规则 (LEGB)

C/C++ 有块作用域。Python **没有块作用域**，只有函数作用域：

```bash
python3 examples/scoping.py
```
