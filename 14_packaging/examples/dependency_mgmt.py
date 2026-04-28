"""
依赖管理深入讲解
"""

import sys
import os

print("=== pip — 基础包管理器 ===")
print("""
常用命令:
  pip install package              # 安装
  pip install package==1.2.3       # 指定版本
  pip install package>=1.2,<2.0    # 版本范围
  pip install -r requirements.txt  # 从文件安装
  pip install -e .                 # 开发模式安装
  pip install -e ".[dev]"          # 开发模式 + 可选依赖

  pip uninstall package            # 卸载
  pip list                         # 列出已安装包
  pip show package                 # 查看包信息
  pip freeze > requirements.txt    # 导出当前环境

  pip install --upgrade pip        # 升级 pip 自身
  pip install --no-cache-dir pkg   # 不使用缓存
  pip install --index-url URL pkg  # 使用镜像源
""".strip())

print("\n\n=== requirements.txt vs pyproject.toml ===")
print("""
requirements.txt（传统方式，精确锁定版本）:
  requests==2.31.0
  click==8.1.7
  pydantic==2.5.0

pyproject.toml [project.dependencies]（现代方式，版本范围）:
  dependencies = [
      "requests>=2.28",
      "click>=8.0",
      "pydantic>=2.0,<3.0",
  ]

最佳实践:
  - pyproject.toml: 声明最小版本要求（类似 CMake 的 find_package 版本要求）
  - requirements.txt 或 lock 文件: 精确锁定版本（可复现环境）
""".strip())

print("\n\n=== 虚拟环境深入 ===")
print("""
Python 的虚拟环境工具:

1. venv（标准库，推荐）:
   python3 -m venv .venv
   source .venv/bin/activate

2. virtualenv（第三方，更多功能）:
   pip install virtualenv
   virtualenv .venv

虚拟环境的原理:
   .venv/
   ├── bin/
   │   ├── python -> /usr/bin/python3    # 符号链接
   │   ├── pip                           # 独立的 pip
   │   └── activate                      # 设置 PATH
   ├── lib/
   │   └── python3.12/
   │       └── site-packages/            # 独立的包目录
   └── pyvenv.cfg                        # 配置文件

   activate 脚本做的事:
   - 修改 PATH，把 .venv/bin 放在最前面
   - 设置 VIRTUAL_ENV 环境变量
   - 修改 shell 提示符
""".strip())

print("\n\n=== Poetry — 现代依赖管理 ===")
print("""
Poetry 类似 Rust 的 Cargo，提供:
  - 依赖解析和锁定
  - 虚拟环境管理
  - 构建和发布

# 安装
pip install poetry

# 创建项目
poetry new myproject
# 或在现有项目中初始化
poetry init

# 添加依赖
poetry add requests
poetry add --group dev pytest

# 安装所有依赖
poetry install

# 运行命令（在虚拟环境中）
poetry run python script.py
poetry run pytest

# 锁定版本
poetry lock

# 构建
poetry build

# 发布到 PyPI
poetry publish

# poetry.lock 文件:
#   类似 npm 的 package-lock.json
#   精确锁定所有依赖的版本
#   应该提交到版本控制
""".strip())

print("\n\n=== uv — 新一代工具 (Rust 实现) ===")
print("""
uv 是 pip 和 venv 的快速替代品:

# 安装
curl -LsSf https://astral.sh/uv/install.sh | sh

# 创建虚拟环境
uv venv

# 安装包（极快！）
uv pip install requests
uv pip install -r requirements.txt

# 项目管理
uv init myproject
uv add requests
uv add --dev pytest
uv run python script.py

# 速度对比:
#   pip install numpy:  ~15s
#   uv pip install numpy: ~1s
""".strip())

print("\n\n=== conda — 科学计算环境 ===")
print("""
conda 不仅管理 Python 包，还管理 C 库和工具:

# 安装（推荐 miniforge）
# https://github.com/conda-forge/miniforge

# 创建环境
conda create -n myenv python=3.12

# 激活
conda activate myenv

# 安装（包含 C/Fortran 编译好的二进制）
conda install numpy scipy matplotlib

# 为什么用 conda:
#   - NumPy/SciPy 依赖 BLAS/LAPACK（C/Fortran 库）
#   - conda 提供预编译的二进制，无需本地编译
#   - pip 安装 NumPy 可能需要编译器
""".strip())

# 显示当前环境信息
print("\n\n=== 当前环境信息 ===")
print(f"Python: {sys.version}")
print(f"可执行文件: {sys.executable}")
print(f"虚拟环境: {os.environ.get('VIRTUAL_ENV', '(未激活)')}")
print(f"PATH 中的 Python:")

import shutil
python_path = shutil.which("python3")
print(f"  python3 → {python_path}")
pip_path = shutil.which("pip3") or shutil.which("pip")
print(f"  pip → {pip_path}")
