"""
类型提示基础

C/C++ 是静态类型语言，类型信息在编译时使用。
Python 的类型提示是注解，不影响运行时，但可以被工具检查。

运行 mypy:
    pip install mypy
    mypy this_file.py
"""

from typing import Optional, Union
from collections.abc import Sequence

print("=== 基本类型注解 ===")

# C: int add(int a, int b) { return a + b; }
def add(a: int, b: int) -> int:
    return a + b

# C: void greet(const char* name) { ... }
def greet(name: str) -> None:
    print(f"  Hello, {name}!")

result: int = add(1, 2)  # 变量注解
print(f"add(1, 2) = {result}")
greet("World")

# 注解不影响运行！以下代码运行正常：
result2 = add("hello", " world")  # mypy 会报错，但运行不会
print(f'add("hello", " world") = {result2}')

print("\n=== 容器类型 ===")
# Python 3.9+ 可以直接用内置类型作为泛型

def average(numbers: list[float]) -> float:
    return sum(numbers) / len(numbers)

def word_count(text: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for word in text.split():
        counts[word] = counts.get(word, 0) + 1
    return counts

print(f"average: {average([1.0, 2.0, 3.0, 4.0])}")
print(f"word_count: {word_count('hello world hello python')}")

print("\n=== Optional 和 Union ===")

# C++ 类似 std::optional<T>
def find_user(user_id: int) -> Optional[str]:
    """Optional[str] 等价于 str | None"""
    users = {1: "Alice", 2: "Bob"}
    return users.get(user_id)

print(f"find_user(1) = {find_user(1)}")
print(f"find_user(99) = {find_user(99)}")

# Union: 多种可能的类型
# Python 3.10+ 可以用 X | Y 语法
def process(value: int | str) -> str:
    if isinstance(value, int):
        return f"整数: {value}"
    return f"字符串: {value}"

print(f"process(42) = {process(42)}")
print(f"process('hi') = {process('hi')}")

print("\n=== 类型别名 ===")

# C++: using Point = std::pair<float, float>;
type Point = tuple[float, float]  # Python 3.12+
# 或: Point = tuple[float, float]

type Matrix = list[list[float]]

def distance(p1: Point, p2: Point) -> float:
    return ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2) ** 0.5

print(f"distance: {distance((0, 0), (3, 4)):.2f}")

print("\n=== Callable 类型 ===")
from collections.abc import Callable

# C++: std::function<int(int, int)>
def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

print(f"apply(add, 3, 4) = {apply(add, 3, 4)}")
print(f"apply(lambda a,b: a*b, 3, 4) = {apply(lambda a, b: a * b, 3, 4)}")

print("\n=== 类中的类型提示 ===")

class Stack:
    """类型化的栈（运行时无泛型约束）"""

    def __init__(self) -> None:
        self._items: list[int] = []

    def push(self, item: int) -> None:
        self._items.append(item)

    def pop(self) -> int:
        return self._items.pop()

    def peek(self) -> int:
        return self._items[-1]

    @property
    def empty(self) -> bool:
        return len(self._items) == 0

s = Stack()
s.push(1)
s.push(2)
s.push(3)
print(f"Stack: peek={s.peek()}, pop={s.pop()}, empty={s.empty}")

print("\n=== 运行时获取类型注解 ===")
# 类型注解可以在运行时访问（通过 __annotations__）
print(f"add 的注解: {add.__annotations__}")
print(f"Stack.push 的注解: {Stack.push.__annotations__}")

# typing.get_type_hints() 解析字符串注解
import typing
hints = typing.get_type_hints(add)
print(f"解析后的注解: {hints}")
