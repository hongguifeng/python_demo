"""
作用域规则 (LEGB)

关键差异：Python 没有块作用域！
C/C++ 中 {} 创建新作用域，Python 只有函数/类/模块作用域。
"""

print("=== Python 没有块作用域 ===")

# C/C++:
# if (true) { int x = 42; }
# printf("%d\n", x);  // 编译错误！x 不在作用域内

# Python:
if True:
    x = 42
print(f"x = {x}")  # 完全合法！x 在 if 外仍然可见

for i in range(5):
    last = i
print(f"循环变量 i = {i}, last = {last}")  # i 和 last 在循环外可用

print("\n=== LEGB 规则 ===")
# L - Local: 函数内部
# E - Enclosing: 外层函数（闭包）
# G - Global: 模块级别
# B - Built-in: Python 内置

global_var = "global"

def outer():
    enclosing_var = "enclosing"

    def inner():
        local_var = "local"
        print(f"  L: {local_var}")
        print(f"  E: {enclosing_var}")
        print(f"  G: {global_var}")
        print(f"  B: {len}")  # len 是内置函数

    inner()

outer()

print("\n=== global 和 nonlocal 关键字 ===")
# 读取外层变量不需要声明，但修改需要

counter = 0

def increment_wrong():
    # counter += 1  # UnboundLocalError!
    # 因为 += 隐含赋值，Python 认为 counter 是局部变量
    pass

def increment_right():
    global counter  # 声明要修改全局变量
    counter += 1

increment_right()
increment_right()
print(f"counter = {counter}")

# nonlocal: 修改闭包中的变量
def make_counter():
    count = 0

    def increment():
        nonlocal count  # 声明要修改外层函数的变量
        count += 1
        return count

    return increment

counter = make_counter()
print(f"\n闭包计数器: {counter()}, {counter()}, {counter()}")

print("\n=== 变量生命周期 ===")
# C++: 变量在作用域结束时析构
# Python: 变量在引用计数归零时销毁（可能延迟）

class Resource:
    def __init__(self, name):
        self.name = name
        print(f"  创建 {self.name}")

    def __del__(self):
        print(f"  销毁 {self.name}")

print("创建资源:")
r = Resource("R1")
print("重新赋值:")
r = Resource("R2")  # R1 的引用计数归零，立即销毁（在 CPython 中）
print("函数结束前")
del r  # 显式删除引用
print("del r 之后")
