"""
list vs C/C++ array

list 是 Python 最常用的数据结构，但和 C 数组有根本区别。
底层实现是动态数组（类似 std::vector<PyObject*>）。
"""

import sys

print("=== 创建 list ===")
# C: int arr[] = {1, 2, 3};
nums = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, [1, 2]]  # 可以存不同类型！

print(f"nums = {nums}")
print(f"mixed = {mixed}")

print("\n=== 基本操作（对比 std::vector）===")
lst = [1, 2, 3]

# push_back
lst.append(4)
print(f"append(4): {lst}")

# insert
lst.insert(0, 0)
print(f"insert(0,0): {lst}")

# pop_back
last = lst.pop()
print(f"pop(): got {last}, list = {lst}")

# pop at index
second = lst.pop(1)
print(f"pop(1): got {second}, list = {lst}")

# remove by value（C++ 的 erase + find）
lst.extend([5, 6, 7])
lst.remove(5)  # 删除第一个值为 5 的元素
print(f"remove(5): {lst}")

# 清空
lst.clear()
print(f"clear(): {lst}")

print("\n=== 内存模型（C 开发者关注）===")
# Python list 是指针数组，不是连续的值数组！
# list = [PyObject*, PyObject*, PyObject*, ...]
# 类似于 C 的 void* arr[]

lst = list(range(10))
print(f"list 内存: {sys.getsizeof(lst)} bytes (10 个元素)")
print(f"  对比: C 的 int[10] = {10 * 4} bytes")
print(f"  开销来源: PyObject* 指针 + 对象头 + 预分配空间")

# 查看预分配行为（类似 vector 的 capacity）
lst2 = []
prev_size = sys.getsizeof(lst2)
for i in range(20):
    lst2.append(i)
    new_size = sys.getsizeof(lst2)
    if new_size != prev_size:
        print(f"  len={len(lst2):2d}, size={new_size:4d} bytes (增长!)")
        prev_size = new_size

print("\n=== 排序（对比 qsort/std::sort）===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# 原地排序（类似 std::sort）
nums.sort()
print(f"sort(): {nums}")

# 自定义排序
words = ["banana", "apple", "cherry", "date"]
words.sort(key=len)  # 按长度排序（key 函数替代 C 的比较函数指针）
print(f"sort(key=len): {words}")

# 不修改原列表的排序
original = [3, 1, 4, 1, 5]
sorted_copy = sorted(original, reverse=True)
print(f"sorted(reverse=True): {sorted_copy}")
print(f"original unchanged: {original}")

print("\n=== list 作为栈和队列 ===")
# 栈（后进先出）— list 天然支持
stack = []
stack.append(1)  # push
stack.append(2)
stack.append(3)
top = stack.pop()  # pop
print(f"栈: push 1,2,3 then pop → {top}, stack = {stack}")

# 队列 — list 的 pop(0) 是 O(n)！用 collections.deque
from collections import deque
queue = deque()
queue.append(1)     # 入队
queue.append(2)
queue.append(3)
first = queue.popleft()  # 出队 O(1)
print(f"队列: enqueue 1,2,3 then dequeue → {first}, queue = {list(queue)}")

print("\n=== list 判等与比较 ===")
# == 比较值（递归），is 比较引用
a = [1, [2, 3]]
b = [1, [2, 3]]
print(f"a == b: {a == b}")  # True（值相同）
print(f"a is b: {a is b}")  # False（不同对象）

# 列表比较是字典序的（类似 strcmp）
print(f"[1,2] < [1,3]: {[1,2] < [1,3]}")
print(f"[1,2] < [2,0]: {[1,2] < [2,0]}")
