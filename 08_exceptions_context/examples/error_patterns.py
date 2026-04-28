"""
错误处理模式与最佳实践
"""

print("=== 模式 1: 哨兵值 vs 异常 ===")

# C 风格：返回错误码/哨兵值
def find_index_c_style(lst, value):
    """返回 -1 表示未找到（像 C 的 convention）"""
    for i, item in enumerate(lst):
        if item == value:
            return i
    return -1

# Python 风格：抛出异常
def find_index_pythonic(lst, value):
    """未找到抛出 ValueError（像 list.index()）"""
    for i, item in enumerate(lst):
        if item == value:
            return i
    raise ValueError(f"{value!r} not in list")

data = [10, 20, 30]
# C 风格使用
idx = find_index_c_style(data, 99)
if idx != -1:
    print(f"找到了: {idx}")
else:
    print("C 风格: 未找到")

# Python 风格使用
try:
    idx = find_index_pythonic(data, 99)
    print(f"找到了: {idx}")
except ValueError:
    print("Python 风格: 未找到")

print("\n=== 模式 2: 异常分组 (Python 3.11+) ===")

# ExceptionGroup 允许同时抛出多个异常
def validate(data):
    errors = []
    if not data.get("name"):
        errors.append(ValueError("name is required"))
    if not isinstance(data.get("age"), int):
        errors.append(TypeError("age must be int"))
    if data.get("age", 0) < 0:
        errors.append(ValueError("age must be non-negative"))
    if errors:
        raise ExceptionGroup("validation failed", errors)

try:
    validate({"name": "", "age": "not_int"})
except ExceptionGroup as eg:
    print(f"异常组 ({len(eg.exceptions)} 个错误):")
    for e in eg.exceptions:
        print(f"  {type(e).__name__}: {e}")

print("\n=== 模式 3: 重试模式 ===")

import time
import random

def retry(func, max_attempts=3, delay=0.01, exceptions=(Exception,)):
    """通用重试函数"""
    for attempt in range(1, max_attempts + 1):
        try:
            return func()
        except exceptions as e:
            if attempt == max_attempts:
                raise
            print(f"  尝试 {attempt} 失败: {e}, 重试...")
            time.sleep(delay)

# 模拟不稳定的操作
call_count = 0
def flaky_operation():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ConnectionError("连接被拒绝")
    return "成功"

call_count = 0
result = retry(flaky_operation)
print(f"重试结果: {result}")

print("\n=== 模式 4: 错误累积 ===")

def process_records(records):
    """处理多条记录，累积错误而非立即失败"""
    results = []
    errors = []

    for i, record in enumerate(records):
        try:
            # 模拟处理
            if record < 0:
                raise ValueError(f"负数: {record}")
            results.append(record ** 2)
        except Exception as e:
            errors.append((i, str(e)))

    return results, errors

data = [1, 2, -3, 4, -5, 6]
results, errors = process_records(data)
print(f"成功结果: {results}")
print(f"错误记录: {errors}")

print("\n=== 模式 5: 确保清理（多重保险）===")

class ManagedResource:
    """展示多层清理保障"""

    def __init__(self, name):
        self.name = name
        self.acquired = True
        print(f"  获取 {self.name}")

    def close(self):
        """显式关闭"""
        if self.acquired:
            self.acquired = False
            print(f"  释放 {self.name}")

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __del__(self):
        if self.acquired:
            import warnings
            warnings.warn(f"ResourceWarning: {self.name} was not closed")
            self.close()

# 最佳实践：使用 with
print("使用 with:")
with ManagedResource("DB连接") as r:
    print(f"  使用 {r.name}")
# 自动关闭

# 手动管理（不推荐但可行）
print("\n手动管理:")
r = ManagedResource("文件句柄")
try:
    print(f"  使用 {r.name}")
finally:
    r.close()
