"""
异常处理基础

C++: try { ... } catch(const std::exception& e) { ... }
Python: try: ... except Exception as e: ...
"""

print("=== 基本 try/except ===")

# C++ 风格：先检查再操作 (LBYL)
# if (divisor != 0) result = dividend / divisor;

# Python 风格：先操作再处理异常 (EAFP)
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return float('inf')

print(f"10 / 3 = {safe_divide(10, 3):.4f}")
print(f"10 / 0 = {safe_divide(10, 0)}")

print("\n=== 完整的 try 语句 ===")

def process_data(data):
    try:
        # 可能抛出异常的代码
        result = int(data)
        value = 100 / result
    except ValueError as e:
        # 捕获特定异常（类似 catch(std::invalid_argument&)）
        print(f"  ValueError: {e}")
        return None
    except ZeroDivisionError:
        print(f"  ZeroDivisionError")
        return None
    except (TypeError, AttributeError) as e:
        # 捕获多种异常
        print(f"  TypeError/AttributeError: {e}")
        return None
    else:
        # 没有异常时执行（C++ 没有这个！）
        print(f"  成功: {value}")
        return value
    finally:
        # 无论如何都执行（和 C++ 类似，但更常用）
        print(f"  finally: 清理完成")

process_data("5")
process_data("abc")
process_data("0")

print("\n=== 异常层次结构 ===")
print("""
BaseException
├── SystemExit           # sys.exit()
├── KeyboardInterrupt    # Ctrl+C
├── GeneratorExit        # generator.close()
└── Exception            # ← 通常只捕获这个
    ├── StopIteration
    ├── ArithmeticError
    │   ├── ZeroDivisionError
    │   └── OverflowError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    ├── OSError
    │   ├── FileNotFoundError
    │   └── PermissionError
    ├── TypeError
    ├── ValueError
    ├── AttributeError
    └── RuntimeError
""".strip())

# 不要捕获 BaseException（会吞掉 Ctrl+C）
# 不要裸 except:（等价于 except BaseException:）

print("\n=== 自定义异常 ===")

class AppError(Exception):
    """应用程序基础异常"""
    pass

class ValidationError(AppError):
    """数据验证错误"""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """资源未找到"""
    def __init__(self, resource, id_):
        self.resource = resource
        self.id = id_
        super().__init__(f"{resource}(id={id_}) not found")

def validate_age(age):
    if not isinstance(age, int):
        raise ValidationError("age", f"expected int, got {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValidationError("age", f"invalid value: {age}")

try:
    validate_age(-5)
except ValidationError as e:
    print(f"验证错误: {e}")
    print(f"  字段: {e.field}")

print("\n=== raise from — 异常链 ===")
# 类似 C++ 的 std::throw_with_nested

def load_config(path):
    try:
        with open(path) as f:
            return f.read()
    except FileNotFoundError as e:
        # 保留原始异常信息
        raise AppError(f"配置文件加载失败: {path}") from e

try:
    load_config("/nonexistent/config.yaml")
except AppError as e:
    print(f"应用错误: {e}")
    print(f"原因: {e.__cause__}")

print("\n=== 异常在循环中使用 ===")
# Python 中异常不仅用于"错误"，还用于流程控制

# StopIteration 是迭代结束的信号
it = iter([1, 2, 3])
while True:
    try:
        print(f"  {next(it)}", end=" ")
    except StopIteration:
        print("(结束)")
        break

# KeyError 是检查字典键的方式
d = {"a": 1}
try:
    v = d["b"]
except KeyError:
    v = "default"
print(f"d['b'] with fallback: {v}")
