# 01 - 运行环境与工具链

> C/C++ 开发者眼中的 `gcc`/`cmake` → Python 的 `python`/`pip`/`venv`

## 核心差异

| 维度 | C/C++ | Python |
|------|-------|--------|
| 执行方式 | 编译为机器码再运行 | 解释执行（字节码编译 + VM） |
| 入口 | `main()` 函数 | 脚本顶层代码 / `__main__` |
| 构建工具 | Makefile / CMake | 无需构建（直接运行） |
| 包管理 | 系统包管理器 / vcpkg / conan | pip / poetry / conda |
| 依赖隔离 | 无原生方案 | 虚拟环境 (venv) |

## 1.1 Python 解释器

Python 不是一门语言的单一实现——它有多个解释器：

| 实现 | 语言 | 特点 |
|------|------|------|
| **CPython** | C | 官方参考实现，最常用 |
| **PyPy** | RPython | JIT 编译，某些场景快 5-10x |
| **Cython** | C 扩展 | 将 Python 编译为 C，用于加速 |
| **MicroPython** | C | 嵌入式系统用 |

对于 C/C++ 开发者的关键认知：**CPython 本身就是一个 C 程序**。你可以把 `python3` 看作一个读取 `.py` 文件并执行的 C 程序，类似于你写的解释器。

```bash
# 查看你的 Python 版本和实现
python3 --version
python3 -c "import sys; print(sys.implementation)"

# 查看 Python 解释器的路径（类似 which gcc）
which python3
python3 -c "import sys; print(sys.executable)"
```

## 1.2 REPL（交互式解释器）

C/C++ 没有原生 REPL（虽然有 `cling`），但 Python 的 REPL 是日常开发利器：

```bash
# 进入交互模式
python3

# 更强大的交互环境
pip install ipython
ipython
```

在 REPL 中可以做到：
- 即时测试表达式和函数
- 用 `dir(obj)` 查看对象的所有属性和方法
- 用 `help(func)` 查看文档
- 用 `type(obj)` 查看类型

运行示例：

```bash
python3 examples/repl_demo.py
```

## 1.3 虚拟环境 (venv)

这是 C/C++ 中没有的概念。想象一下每个项目有独立的 `/usr/lib` 和 `/usr/include`：

```bash
# 创建虚拟环境（类似于创建一个独立的 Python "安装"）
python3 -m venv myproject_env

# 激活（修改 PATH，使 python 指向虚拟环境中的解释器）
source myproject_env/bin/activate  # Linux/macOS
# myproject_env\Scripts\activate   # Windows

# 此时 pip install 的包只存在于这个环境中
pip install requests

# 查看当前环境的包
pip list

# 导出依赖（类似于 CMakeLists.txt 中的 find_package）
pip freeze > requirements.txt

# 从 requirements.txt 复现环境
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

### 为什么需要虚拟环境？

C/C++ 的库是编译时链接的，版本冲突在编译期暴露。Python 的库是运行时导入的：

```
项目 A 需要 requests==2.28
项目 B 需要 requests==2.31
```

没有虚拟环境，它们共享同一个 `site-packages`，必然冲突。

## 1.4 pip — Python 的包管理器

| pip 命令 | 类比 |
|----------|------|
| `pip install pkg` | `apt install` / `vcpkg install` |
| `pip install pkg==1.2.3` | 指定版本安装 |
| `pip install -e .` | 开发模式安装（类似 `cmake --install` 到本地） |
| `pip uninstall pkg` | 卸载 |
| `pip show pkg` | 查看包信息 |
| `pip install -r requirements.txt` | 批量安装依赖 |

## 1.5 项目结构对比

### C/C++ 典型项目

```
myproject/
├── CMakeLists.txt
├── include/
│   └── mylib.h
├── src/
│   ├── main.cpp
│   └── mylib.cpp
├── tests/
│   └── test_mylib.cpp
└── build/
```

### Python 典型项目

```
myproject/
├── pyproject.toml          # 替代 CMakeLists.txt
├── src/
│   └── mypackage/
│       ├── __init__.py     # 标记为包（类似头文件的作用）
│       ├── core.py
│       └── utils.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── requirements.txt        # 依赖列表
└── README.md
```

## 1.6 执行方式

```bash
# 直接运行脚本（最常见）
python3 script.py

# 运行模块（-m 标志）
python3 -m pytest          # 运行测试框架
python3 -m http.server     # 启动简易 HTTP 服务器
python3 -m json.tool < data.json  # JSON 格式化

# 运行包
python3 -m mypackage       # 会执行 mypackage/__main__.py

# 单行执行（类似 gcc -E 做预处理查看）
python3 -c "print(2**100)"
```

运行示例查看字节码（Python 的"目标文件"）：

```bash
python3 examples/bytecode_demo.py
```

## 1.7 `.pyc` 与字节码

C/C++ 有 `.o` 目标文件，Python 有 `.pyc` 字节码缓存：

```
.py  →  字节码(.pyc)  →  Python VM 执行
.c   →  目标文件(.o)   →  链接 → 机器码执行
```

`.pyc` 存放在 `__pycache__/` 目录中，是自动生成的缓存，可以安全删除。

运行示例：

```bash
python3 examples/show_environment.py
```
