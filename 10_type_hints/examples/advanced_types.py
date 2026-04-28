"""
高级类型特性

对应 C++ 的模板、概念 (Concepts)、constexpr 等。
"""

from typing import TypeVar, Generic, Protocol, Final, Literal, TypeGuard
from typing import overload, runtime_checkable
from dataclasses import dataclass

print("=== 泛型 (Generic) — 类似 C++ 模板 ===")

T = TypeVar('T')

class Stack(Generic[T]):
    """
    类似 C++ 的:
    template<typename T>
    class Stack { ... };
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def __repr__(self) -> str:
        return f"Stack({self._items})"

# 使用（类型参数是给 mypy 看的，运行时不检查）
int_stack: Stack[int] = Stack()
int_stack.push(1)
int_stack.push(2)
print(f"int_stack: {int_stack}")

str_stack: Stack[str] = Stack()
str_stack.push("hello")
str_stack.push("world")
print(f"str_stack: {str_stack}")

print("\n=== 泛型函数 ===")

def first(items: list[T]) -> T:
    """类似 C++ 的 template<typename T> T first(vector<T>&)"""
    return items[0]

print(f"first([1,2,3]) = {first([1, 2, 3])}")
print(f"first(['a','b']) = {first(['a', 'b'])}")

# 有界类型变量（类似 C++ 的 concept 约束）
from typing import SupportsFloat

N = TypeVar('N', int, float)  # 只允许 int 或 float

def clamp(value: N, minimum: N, maximum: N) -> N:
    return max(minimum, min(value, maximum))

print(f"clamp(15, 0, 10) = {clamp(15, 0, 10)}")
print(f"clamp(3.5, 0.0, 10.0) = {clamp(3.5, 0.0, 10.0)}")

print("\n=== Protocol — 结构化子类型 ===")
# 类似 C++20 的 Concept，但在运行时也可检查

@runtime_checkable
class Sizeable(Protocol):
    def __len__(self) -> int: ...

class MyContainer:
    def __init__(self, items: list):
        self.items = items
    def __len__(self) -> int:
        return len(self.items)

# 不需要继承 Sizeable！只要有 __len__ 方法就行
def print_size(obj: Sizeable) -> None:
    print(f"  {type(obj).__name__}: size = {len(obj)}")

print_size([1, 2, 3])
print_size("hello")
print_size(MyContainer([1, 2]))

# 运行时检查
print(f"list 是 Sizeable: {isinstance([], Sizeable)}")
print(f"int 是 Sizeable: {isinstance(42, Sizeable)}")

print("\n=== Final — 类似 const ===")

MAX_SIZE: Final[int] = 100
# MAX_SIZE = 200  # mypy 会报错（运行时不阻止）
print(f"MAX_SIZE = {MAX_SIZE}")

print("\n=== Literal — 字面量类型 ===")
# 类似 C++ 的 enum，但更灵活

def set_mode(mode: Literal["read", "write", "append"]) -> str:
    return f"模式设置为: {mode}"

print(set_mode("read"))
# set_mode("invalid")  # mypy 会报错

print("\n=== TypeGuard — 类型收窄 ===")
# 类似 C++ 的 dynamic_cast 成功后的类型保证

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

data: list[object] = ["hello", "world"]
if is_string_list(data):
    # 在这个分支中，mypy 知道 data 是 list[str]
    print(f"字符串列表: {', '.join(data)}")

print("\n=== @overload — 函数重载 ===")
# C++ 的函数重载是真实的。Python 的 @overload 只是给 mypy 的提示。

@overload
def double(x: int) -> int: ...
@overload
def double(x: str) -> str: ...

def double(x: int | str) -> int | str:
    if isinstance(x, int):
        return x * 2
    return x + x

print(f"double(5) = {double(5)}")
print(f"double('hi') = {double('hi')}")

print("\n=== 新式泛型语法 (Python 3.12+) ===")
print("""
# Python 3.12+ 的简洁语法:

def first[T](items: list[T]) -> T:
    return items[0]

class Stack[T]:
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

type Point = tuple[float, float]
type Matrix[T] = list[list[T]]

# 不再需要 TypeVar！
""".strip())

print("\n=== 类型检查工具 ===")
print("""
工具:
  mypy:    pip install mypy && mypy script.py
  pyright: pip install pyright && pyright script.py
  pylance: VS Code 扩展（基于 pyright）

常用 mypy 配置 (mypy.ini):
  [mypy]
  python_version = 3.12
  strict = true
  warn_return_any = true
  warn_unused_configs = true

严格模式会检查:
  - 所有函数必须有类型注解
  - 不允许隐式 Any
  - 不允许未类型化的装饰器
""".strip())
