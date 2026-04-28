"""
切片 (Slicing) — Python 序列操作的核心

C/C++ 没有内建切片，需要手动管理指针和长度。
Python 的切片语法统一适用于 list, tuple, str, bytes 等。
"""

print("=== 基本切片语法: seq[start:stop:step] ===")
lst = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
print(f"原始: {lst}")

# 基本切片（左闭右开，和 C++ 的 iterator range 一样）
print(f"lst[2:5]   = {lst[2:5]}")     # [2, 3, 4]
print(f"lst[:3]    = {lst[:3]}")       # [0, 1, 2]  省略 start = 从头开始
print(f"lst[7:]    = {lst[7:]}")       # [7, 8, 9]  省略 stop = 到末尾
print(f"lst[:]     = {lst[:]}")        # 浅拷贝

# 负索引（C 没有！）
print(f"\nlst[-1]    = {lst[-1]}")      # 最后一个
print(f"lst[-3:]   = {lst[-3:]}")      # 最后三个
print(f"lst[:-2]   = {lst[:-2]}")      # 去掉最后两个

# 步长
print(f"\nlst[::2]   = {lst[::2]}")     # 偶数位置
print(f"lst[1::2]  = {lst[1::2]}")     # 奇数位置
print(f"lst[::-1]  = {lst[::-1]}")     # 反转！
print(f"lst[8:2:-1]= {lst[8:2:-1]}")   # 从8到3，反向

print("\n=== 切片赋值（修改原列表）===")
# 这在 C 中需要 memmove + 可能的 realloc
lst = [0, 1, 2, 3, 4, 5]

# 替换一段
lst[1:3] = [10, 20]
print(f"lst[1:3] = [10, 20]: {lst}")

# 插入（替换长度为 0 的切片）
lst[2:2] = [15, 16, 17]
print(f"lst[2:2] = [15,16,17]: {lst}")

# 删除（用空列表替换）
lst[1:4] = []
print(f"lst[1:4] = []: {lst}")

# 替换为不同长度
lst = [1, 2, 3, 4, 5]
lst[1:4] = [20, 30]
print(f"lst[1:4] = [20, 30]: {lst}")

print("\n=== slice 对象 ===")
# 切片可以保存为对象重复使用（类似 C 中保存偏移量和长度）
first_three = slice(0, 3)
last_two = slice(-2, None)

data = [10, 20, 30, 40, 50]
print(f"data[first_three] = {data[first_three]}")
print(f"data[last_two]    = {data[last_two]}")

# NumPy 风格的多维索引就是基于 slice 对象
print(f"slice(1, 10, 2) → start={first_three.start}, stop={first_three.stop}, step={first_three.step}")

print("\n=== 字符串切片 ===")
s = "Hello, World!"
print(f"s[7:12]  = {s[7:12]!r}")
print(f"s[::-1]  = {s[::-1]!r}")
print(f"s[::2]   = {s[::2]!r}")

# 实际应用
url = "https://example.com/path/to/resource"
protocol = url[:url.index("://")]
print(f"\nURL 协议: {protocol!r}")

print("\n=== 切片的时间复杂度 ===")
# 切片创建新列表: O(k) 其中 k 是切片长度
# 这和 C 的 memcpy 类似
# 不像 Go 的 slice 那样共享底层数组
import sys

original = list(range(1000))
sliced = original[100:200]
print(f"original id: {id(original)}")
print(f"sliced   id: {id(sliced)}")
print(f"sliced 是独立对象: {original is not sliced}")

# 修改切片不影响原列表
sliced[0] = 999
print(f"original[100] = {original[100]} (未受影响)")
