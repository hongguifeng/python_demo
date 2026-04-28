# 14 - 包管理与项目工程化

> C/C++ 的 CMake/Makefile vs Python 的 pip/pyproject.toml

## 核心对比

| C/C++ | Python |
|-------|--------|
| CMakeLists.txt | pyproject.toml |
| Makefile | 无需（直接运行） |
| vcpkg / conan | pip / poetry / conda |
| #include path | sys.path / PYTHONPATH |
| .o + .a + .so | .whl (wheel) |
| `cmake .. && make` | `pip install .` |

## 工具生态

| 工具 | 用途 | 类比 |
|------|------|------|
| pip | 包安装 | apt-get / vcpkg |
| venv | 环境隔离 | 无直接等价 |
| poetry | 依赖管理 + 构建 + 发布 | cargo (Rust) |
| conda | 科学计算环境 | 系统包管理器 |
| uv | 快速包管理器 (Rust 实现) | 新一代工具 |

## 示例

```bash
python3 examples/project_structure.py   # 项目结构
python3 examples/dependency_mgmt.py     # 依赖管理
```
