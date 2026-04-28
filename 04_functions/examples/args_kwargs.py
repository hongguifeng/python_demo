"""
*args 和 **kwargs — Python 灵活的参数机制

C/C++ 有 va_list (variadic functions)，但类型不安全。
Python 的可变参数更安全、更强大。
"""

print("=== 位置参数和关键字参数 ===")

def connect(host, port, timeout=30, use_ssl=False):
    """
    C 中没有关键字参数，只有位置参数。
    C++ 没有原生关键字参数（可以用 builder 模式模拟）。
    """
    print(f"  连接 {host}:{port} (timeout={timeout}, ssl={use_ssl})")

# 位置参数
connect("localhost", 8080)
# 关键字参数（可以乱序！）
connect("localhost", 8080, use_ssl=True, timeout=60)
# 混合使用
connect("localhost", 8080, 10)

print("\n=== 默认参数的坑 ===")

# 危险：可变默认参数！
def append_to(element, target=[]):
    """C++ 开发者注意：默认值在函数定义时创建一次，不是每次调用！"""
    target.append(element)
    return target

print(f"第一次调用: {append_to(1)}")
print(f"第二次调用: {append_to(2)}")  # [1, 2] 不是 [2]！

# 正确做法
def append_to_fixed(element, target=None):
    if target is None:
        target = []
    target.append(element)
    return target

print(f"\n修正后第一次: {append_to_fixed(1)}")
print(f"修正后第二次: {append_to_fixed(2)}")

print("\n=== *args — 可变位置参数 ===")

def sum_all(*args):
    """接受任意数量的位置参数，打包为 tuple"""
    print(f"  args = {args}, type = {type(args).__name__}")
    return sum(args)

print(f"sum_all(1,2,3) = {sum_all(1, 2, 3)}")
print(f"sum_all(1,2,3,4,5) = {sum_all(1, 2, 3, 4, 5)}")

# 展开列表传参（类似 C 中展开数组为参数）
nums = [1, 2, 3, 4, 5]
print(f"sum_all(*nums) = {sum_all(*nums)}")

print("\n=== **kwargs — 可变关键字参数 ===")

def create_tag(tag, **attrs):
    """接受任意关键字参数，打包为 dict"""
    attr_str = " ".join(f'{k}="{v}"' for k, v in attrs.items())
    return f"<{tag} {attr_str}>" if attrs else f"<{tag}>"

print(create_tag("div", id="main", class_name="container"))
print(create_tag("img", src="photo.jpg", alt="photo", width="100"))

print("\n=== 参数顺序规则 ===")

def full_example(pos1, pos2, /, normal, *, kw_only, **kwargs):
    """
    pos1, pos2: 仅位置参数（/ 之前）— Python 3.8+
    normal: 普通参数（可位置可关键字）
    kw_only: 仅关键字参数（* 之后）
    **kwargs: 剩余关键字参数
    """
    print(f"  pos1={pos1}, pos2={pos2}, normal={normal}, kw_only={kw_only}")
    if kwargs:
        print(f"  extra kwargs: {kwargs}")

full_example(1, 2, normal=3, kw_only=4, extra="hello")
full_example(1, 2, 3, kw_only=4)

# 仅位置参数的用途：允许 kwargs 中出现同名参数
def example(name, /, **kwargs):
    print(f"  name={name}, kwargs={kwargs}")

example("test", name="in_kwargs")  # 不冲突！

print("\n=== 参数解包 ===")
def point_distance(x1, y1, x2, y2):
    return ((x2 - x1)**2 + (y2 - y1)**2) ** 0.5

# 从序列解包
p1 = (0, 0)
p2 = (3, 4)
dist = point_distance(*p1, *p2)
print(f"距离 {p1} 到 {p2}: {dist}")

# 从字典解包
config = {"x1": 1, "y1": 1, "x2": 4, "y2": 5}
dist = point_distance(**config)
print(f"距离: {dist}")
