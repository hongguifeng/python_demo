# 13 - 与 C/C++ 互操作

> 从 Python 调用 C，从 C 调用 Python

## 为什么互操作？

- **性能关键路径**用 C/C++ 实现
- **复用现有 C 库**（OpenSSL、SQLite、系统调用等）
- **嵌入 Python**到 C/C++ 应用中（脚本引擎）

## 方案对比

| 方案 | 复杂度 | 性能 | 适用场景 |
|------|--------|------|----------|
| `ctypes` | 低 | 中 | 调用现有 C 动态库 |
| `cffi` | 低 | 高 | 替代 ctypes |
| C Extension | 高 | 最高 | CPython 原生扩展 |
| `pybind11` | 中 | 高 | C++ 绑定（推荐） |
| `Cython` | 中 | 高 | 加速 Python 代码 |

## 示例

```bash
python3 examples/ctypes_demo.py    # ctypes 调用 C 库
python3 examples/c_extension.py    # C 扩展入门
```
