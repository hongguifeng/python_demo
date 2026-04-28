# Python for C/C++ Developers

> 面向熟悉 C/C++ 等编译型语言的开发者的 Python 教程

## 设计理念

本教程 **不是** 零基础编程入门。假定你已经熟悉：
- 变量、循环、条件、函数、指针/引用等基本概念
- 编译-链接-运行的工作流程
- 面向对象编程（类、继承、多态）
- 基本的内存管理（堆/栈、malloc/free、RAII）

本教程聚焦于：
- Python 与 C/C++ 的**核心差异**
- Python 作为动态语言的**独特特性**
- **实际工程实践**（环境管理、包管理、项目结构）

## 目录

| 章节 | 主题 | 关键对比 |
|------|------|----------|
| [01](01_environment/README.md) | 运行环境与工具链 | gcc/cmake vs python/pip/venv |
| [02](02_syntax_basics/README.md) | 语法差异速览 | 动态类型、缩进、一切皆对象 |
| [03](03_data_model/README.md) | 数据模型与内置类型 | array/struct vs list/dict/tuple |
| [04](04_functions/README.md) | 函数、闭包与装饰器 | 函数指针 vs 一等公民函数 |
| [05](05_oop/README.md) | 面向对象与鸭子类型 | vtable vs duck typing/MRO |
| [06](06_memory/README.md) | 内存管理与对象生命周期 | malloc/RAII vs 引用计数/GC |
| [07](07_iterators_generators/README.md) | 迭代器与生成器 | iterator pattern vs yield |
| [08](08_exceptions_context/README.md) | 异常处理与上下文管理器 | RAII vs with statement |
| [09](09_modules_packages/README.md) | 模块与包系统 | #include/链接 vs import |
| [10](10_type_hints/README.md) | 类型提示与静态分析 | 静态类型 vs 渐进式类型 |
| [11](11_concurrency/README.md) | 并发与并行编程 | pthread vs GIL/asyncio |
| [12](12_metaprogramming/README.md) | 元编程 | 模板/宏 vs metaclass/descriptor |
| [13](13_c_interop/README.md) | 与 C/C++ 互操作 | ctypes/cffi/pybind11 |
| [14](14_packaging/README.md) | 包管理与项目工程化 | CMakeLists vs pyproject.toml |
| [15](15_performance/README.md) | 性能分析与优化 | valgrind/perf vs cProfile |

## 环境要求

- Python 3.10+（推荐 3.12）
- 操作系统：Linux / macOS / Windows

## 如何使用

```bash
# 每章都有独立的示例代码可以直接运行
cd 01_environment/examples
python3 hello.py

# 或者一次性运行某章的全部示例
cd 03_data_model/examples
for f in *.py; do echo "=== $f ==="; python3 "$f"; echo; done
```
