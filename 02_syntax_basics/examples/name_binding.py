"""
名字绑定 vs 内存复制 —— Python 与 C 的根本差异

C 思维：变量 = 内存盒子（装数据）
Python 思维：变量 = 名字标签（贴在对象上）
"""

print("=== 不可变对象（int）的绑定 ===")
x = 42
y = x
print(f"x = {x}, y = {y}")
print(f"id(x) = {id(x):#x}, id(y) = {id(y):#x}  (指向同一对象)")
print(f"x is y: {x is y}")

x = 100  # x 重新绑定，y 不受影响
print(f"\n修改 x = 100 后:")
print(f"x = {x}, y = {y}")
print(f"id(x) = {id(x):#x}, id(y) = {id(y):#x}  (现在指向不同对象)")

print("\n=== 可变对象（list）的绑定 ===")
a = [1, 2, 3]
b = a       # b 和 a 指向同一个 list 对象！
print(f"a = {a}")
print(f"b = {b}")
print(f"a is b: {a is b}")

a.append(4)  # 修改 a 指向的对象
print(f"\na.append(4) 后:")
print(f"a = {a}")
print(f"b = {b}   ← b 也变了！因为 a 和 b 是同一个对象")

# 这是 C/C++ 开发者最常犯的错误：
# 在 C 中 b = a 是值拷贝，在 Python 中是引用共享

print("\n=== 正确的复制方式 ===")
a = [1, 2, 3]
b = a.copy()    # 浅拷贝（类似 memcpy）
c = list(a)     # 另一种浅拷贝
d = a[:]        # 切片拷贝

a.append(4)
print(f"a = {a}")
print(f"b = {b}   ← 不受影响")
print(f"c = {c}   ← 不受影响")
print(f"d = {d}   ← 不受影响")

print("\n=== 深拷贝 vs 浅拷贝 ===")
import copy

nested = [[1, 2], [3, 4]]
shallow = nested.copy()     # 浅拷贝：外层新建，内层共享
deep = copy.deepcopy(nested)  # 深拷贝：全部新建

nested[0].append(99)
print(f"original: {nested}")
print(f"shallow:  {shallow}  ← 内层对象被影响了！")
print(f"deep:     {deep}     ← 完全独立")
