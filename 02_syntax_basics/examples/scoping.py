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

print("\n=== 同名变量的遮蔽（Shadowing）===")
# 内层作用域的同名变量会遮蔽外层，查找顺序严格按 L→E→G→B

x = "global x"

def shadow_demo():
    x = "enclosing x"          # 遮蔽全局 x

    def inner_shadow():
        x = "local x"          # 遮蔽 enclosing x
        print(f"  inner sees:     x = {x!r}")   # local x

    def inner_no_shadow():
        print(f"  no-shadow sees: x = {x!r}")   # enclosing x

    inner_shadow()
    inner_no_shadow()
    print(f"  outer sees:     x = {x!r}")       # enclosing x

shadow_demo()
print(f"module sees:      x = {x!r}")           # global x

# 内置名称同样可被遮蔽（但强烈不建议！）
def bad_shadow():
    len = lambda s: "oops"     # 遮蔽内置 len
    print(f"  shadowed len([1,2,3]) = {len([1,2,3])!r}")

bad_shadow()
print(f"  built-in len([1,2,3]) = {len([1,2,3])}")  # 全局 len 未受影响

print("\n=== 同名变量：修改时的陷阱 ===")
# 关键规则：函数体内只要出现对某名字的赋值，Python 编译时就把它标记为局部变量。
# 即使赋值在读取之后，读取那行也会因"局部变量未赋值"而抛 UnboundLocalError。

val = 100

def read_only():
    print(f"  读取外层 val = {val}")   # 没有赋值 → 正常走 G，输出 100

def modify_without_declare():
    try:
        print(val)          # 看起来像读取，但下一行有赋值……
    except UnboundLocalError as e:
        print(f"  UnboundLocalError: {e}")
    val = 200               # 这行让 Python 把整个函数里的 val 视为局部变量

def modify_with_global():
    global val
    val += 1                # 正确修改全局变量
    print(f"  global 修改后 val = {val}")

read_only()
modify_without_declare()    # 演示陷阱
modify_with_global()
print(f"模块级 val = {val}")  # 被 modify_with_global 改为 101

# nonlocal 的同名修改陷阱与此完全对称
def outer_val():
    v = 10

    def inner_trap():
        try:
            print(v)        # v 在下方有赋值 → UnboundLocalError
        except UnboundLocalError as e:
            print(f"  nonlocal 陷阱 UnboundLocalError: {e}")
        v = 20

    def inner_fix():
        nonlocal v
        v += 5              # 正确修改 enclosing v
        print(f"  nonlocal 修改后 v = {v}")

    inner_trap()
    inner_fix()
    print(f"  outer v = {v}")  # 被 inner_fix 改为 15

outer_val()

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
