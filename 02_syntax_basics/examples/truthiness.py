"""
Python 真值判断

C/C++ 只有 0/非零。Python 有更丰富的 falsy/truthy 值。
"""

print("=== Falsy 值 ===")
falsy_values = [None, False, 0, 0.0, 0j, "", [], (), {}, set(), frozenset()]
for v in falsy_values:
    assert not v, f"{v!r} should be falsy"
    print(f"  bool({v!r:20s}) = {bool(v)}")

print("\n=== Truthy 值 ===")
truthy_values = [True, 1, -1, 0.1, "hello", [0], (0,), {"": ""}, {0}]
for v in truthy_values:
    assert v, f"{v!r} should be truthy"
    print(f"  bool({v!r:20s}) = {bool(v)}")

# 实际应用：简洁的空值检查
print("\n=== 实际应用 ===")

# C 风格（繁琐）
items = []
if len(items) == 0:
    print("  C 风格: items 为空")

# Python 风格（惯用法）
if not items:
    print("  Python 风格: items 为空")

# None 检查
value = None
# C 风格
if value is None:  # 推荐用 is None 而非 == None
    print("  value is None")

# 短路求值（和 C 一样）
print("\n=== 短路求值 ===")
# or 返回第一个 truthy 值，and 返回第一个 falsy 值
name = "" or "default"
print(f'  "" or "default" = {name!r}')

result = "hello" and "world"
print(f'  "hello" and "world" = {result!r}')

result = "" and "world"
print(f'  "" and "world" = {result!r}')

# 三元运算符
print("\n=== 三元运算符 ===")
# C:   int y = (x > 0) ? x : -x;
# Python:
x = -5
y = x if x > 0 else -x
print(f"  x = {x}, abs = {y}")
