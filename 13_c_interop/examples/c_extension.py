"""
C 扩展模块入门 — 构建和使用指南

本文件不是可直接运行的 C 扩展，而是讲解如何创建 C 扩展。
"""

print("=== C 扩展模块概述 ===")
print("""
C 扩展是 CPython 的原生插件机制。
NumPy、pandas 等库的核心都是 C 扩展。

三种创建方式:
  1. CPython C API（最底层，直接操作 PyObject*）
  2. Cython（Python 超集编译为 C）
  3. pybind11（C++ header-only 库）
""")

print("\n=== 方式 1: CPython C API ===")
print("""
// mymodule.c
#include <Python.h>

// C 函数实现
static PyObject* mymodule_add(PyObject* self, PyObject* args) {
    int a, b;
    if (!PyArg_ParseTuple(args, "ii", &a, &b))
        return NULL;
    return PyLong_FromLong(a + b);
}

// 方法表
static PyMethodDef MyMethods[] = {
    {"add", mymodule_add, METH_VARARGS, "Add two integers"},
    {NULL, NULL, 0, NULL}
};

// 模块定义
static struct PyModuleDef mymodule = {
    PyModuleDef_HEAD_INIT,
    "mymodule",
    "My C extension module",
    -1,
    MyMethods
};

// 模块初始化
PyMODINIT_FUNC PyInit_mymodule(void) {
    return PyModule_Create(&mymodule);
}
""".strip())

print("\n\n=== 方式 2: Cython（推荐加速 Python 代码）===")
print("""
# fibonacci.pyx
def fib(int n):
    cdef int a = 0, b = 1
    cdef int i
    for i in range(n):
        a, b = b, a + b
    return a

# setup.py
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize("fibonacci.pyx"))

# 编译: python setup.py build_ext --inplace
# 使用: from fibonacci import fib
""".strip())

print("\n\n=== 方式 3: pybind11（推荐 C++ 绑定）===")
print("""
// mylib.cpp
#include <pybind11/pybind11.h>
namespace py = pybind11;

int add(int a, int b) { return a + b; }

class Vector {
public:
    double x, y;
    Vector(double x, double y) : x(x), y(y) {}
    double norm() { return sqrt(x*x + y*y); }
};

PYBIND11_MODULE(mylib, m) {
    m.def("add", &add, "Add two numbers");

    py::class_<Vector>(m, "Vector")
        .def(py::init<double, double>())
        .def_readwrite("x", &Vector::x)
        .def_readwrite("y", &Vector::y)
        .def("norm", &Vector::norm);
}

# 编译（使用 CMake 或 setup.py）
# pip install pybind11
# c++ -O3 -shared -std=c++17 -fPIC $(python3 -m pybind11 --includes) mylib.cpp -o mylib$(python3-config --extension-suffix)
""".strip())

print("\n\n=== 已有的 C 扩展示例 ===")
# Python 标准库中很多模块都是 C 扩展

import _json
print(f"_json (C 实现): {_json.__file__}")

import _collections
print(f"_collections (C): 包含 deque 等高性能容器")

# 查看模块是否是 C 扩展
import json
import collections

print(f"\njson 加速器: {hasattr(json, '_default_encoder')}")

print("\n=== struct 模块 — 二进制数据处理 ===")
import struct

# 类似 C 的二进制读写
# 打包（Python → bytes）
data = struct.pack('iif', 1, 2, 3.14)  # int, int, float
print(f"打包: {data.hex()}")
print(f"大小: {len(data)} bytes")

# 解包（bytes → Python）
a, b, c = struct.unpack('iif', data)
print(f"解包: a={a}, b={b}, c={c:.2f}")

# 网络字节序
data_be = struct.pack('!HI', 80, 12345)  # ! = 网络字节序 (big-endian)
port, addr = struct.unpack('!HI', data_be)
print(f"\n网络字节序: port={port}, addr={addr}")

# 计算结构体大小
print(f"struct.calcsize('iif') = {struct.calcsize('iif')} bytes")
print(f"struct.calcsize('!HI') = {struct.calcsize('!HI')} bytes")

print("\n=== 性能对比概览 ===")
import time

def python_sum(n):
    total = 0
    for i in range(n):
        total += i
    return total

N = 1_000_000

start = time.perf_counter()
r1 = python_sum(N)
t_python = time.perf_counter() - start

start = time.perf_counter()
r2 = sum(range(N))  # C 实现的 sum + range
t_builtin = time.perf_counter() - start

print(f"纯 Python 循环: {t_python:.4f}s")
print(f"内置 sum+range:  {t_builtin:.4f}s")
print(f"加速比: {t_python/t_builtin:.0f}x")
print(f"(内置函数是 C 实现的，所以快很多)")
