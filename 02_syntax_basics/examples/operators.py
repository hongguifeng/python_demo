"""
运算符差异

Python 的运算符与 C/C++ 有一些关键区别。
"""

print("=== 算术运算符 ===")
# 除法！这是最大的坑
print(f"7 / 2  = {7 / 2}")     # 真除法，返回 float（C 中是整数除法！）
print(f"7 // 2 = {7 // 2}")    # 地板除法（类似 C 的整数除法）
print(f"7 % 2  = {7 % 2}")     # 取模

# 幂运算（C 中需要 pow()）
print(f"2 ** 10 = {2 ** 10}")
print(f"2 ** 100 = {2 ** 100}")  # 大整数！

# 负数取模的区别
print(f"\n负数取模:")
print(f"Python: -7 % 3 = {-7 % 3}")    # 结果为 2（向负无穷取整）
print(f"C/C++:  -7 % 3 = -1（向零取整）")  # C 的结果

print("\n=== 比较运算符 ===")
# 链式比较（C 没有！）
x = 5
print(f"1 < {x} < 10: {1 < x < 10}")          # Python 独有
print(f"1 < {x} and {x} < 10: {1 < x and x < 10}")  # 等价的 C 风格

# is vs ==
a = [1, 2, 3]
b = [1, 2, 3]
print(f"\na == b: {a == b}")    # 值相等（类似 C++ operator==）
print(f"a is b: {a is b}")      # 同一对象（类似比较指针地址）

# 注意：小整数缓存
x = 256
y = 256
print(f"\n256 is 256: {x is y}")   # True（CPython 缓存 -5 到 256）
x = 257
y = 257
# 注意：在脚本中这可能为 True（编译器优化），在 REPL 中可能为 False

print("\n=== 逻辑运算符 ===")
# C: &&, ||, !
# Python: and, or, not
print(f"True and False: {True and False}")
print(f"True or False:  {True or False}")
print(f"not True:       {not True}")

# and/or 返回的是操作数，不是 bool！
print(f"\n'hello' or 'world': {'hello' or 'world'!r}")  # 'hello'
print(f"'' or 'world':      {'' or 'world'!r}")          # 'world'
print(f"'hello' and 'world': {'hello' and 'world'!r}")  # 'world'
print(f"'' and 'world':      {'' and 'world'!r}")        # ''

print("\n=== 位运算符（和 C 一样）===")
print(f"0xFF & 0x0F = {0xFF & 0x0F:#04x}")
print(f"0x0F | 0xF0 = {0x0F | 0xF0:#04x}")
print(f"0xFF ^ 0x0F = {0xFF ^ 0x0F:#04x}")
print(f"~0x00 = {~0x00}")       # -1（Python int 没有固定位宽！）
print(f"1 << 10 = {1 << 10}")

print("\n=== 没有的运算符 ===")
# Python 没有: ++, --, ?:（三元用 x if cond else y）
# Python 没有: -> (用 . 代替), :: (用 . 代替)
# Python 没有: sizeof（用 sys.getsizeof）

# 增量赋值
x = 10
x += 1   # 有
# x++     # 没有！这不是语法错误，但 ++x 会被解析为 +(+x)
print(f"x += 1: x = {x}")

print("\n=== 海象运算符 := (Python 3.8+) ===")
# 在表达式中赋值（类似 C 的 if ((x = func()) != NULL)）
data = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# 传统写法
filtered = [x for x in data if x ** 2 > 50]
# 海象运算符：避免重复计算
filtered_walrus = [y for x in data if (y := x ** 2) > 50]

print(f"x^2 > 50 的结果: {filtered_walrus}")
