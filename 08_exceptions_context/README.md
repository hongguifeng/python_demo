# 08 - 异常处理与上下文管理器

> C++ 的 RAII / try-catch vs Python 的 with / try-except

## 核心差异

| C++ | Python |
|-----|--------|
| RAII（析构函数自动清理） | `with` 语句（上下文管理器） |
| `try/catch/throw` | `try/except/raise` |
| 异常规范（已废弃） | 无异常声明（任何函数可以抛出异常） |
| 返回错误码是常见模式 | 异常是**首选**的错误处理方式 |
| `std::exception` 层次 | `BaseException` 层次 |
| `noexcept` | 无等价物 |

## Python 的异常哲学

C++ 社区对异常有争议（性能开销、流程控制）。
Python 社区拥抱异常：**EAFP > LBYL**。

## 示例

```bash
python3 examples/exception_basics.py  # 异常基础
python3 examples/context_manager.py   # 上下文管理器
python3 examples/error_patterns.py    # 错误处理模式
```
