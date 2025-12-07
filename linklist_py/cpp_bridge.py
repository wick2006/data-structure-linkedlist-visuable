# linklist_py/cpp_bridge.py
"""
ctypes 桥接模块：加载 linkedlist.dll
并提供一个进程级的链表管理器（UUID -> handle）。
如果 DLL 无法加载，会回退到纯 Python 实现（linked_list.LinkedListPY）。
"""

import ctypes
import threading
import uuid
import os
import sys
from ctypes import c_int, c_void_p, POINTER
from typing import List, Optional

try:
    from .linked_list import LinkedListPY
except Exception:
    # 相对导入失败时尝试顶层导入（方便独立测试）
    from linked_list import LinkedListPY

_lock = threading.Lock()
_lists = {}  # id -> handle (c_void_p) 或 Python 实例
_using_cpp = False
_lib = None

def _load_dll():
    global _using_cpp, _lib
    if _lib is not None:
        return
    # 预测 DLL 在项目的 libs/ 目录中（相对于当前文件）
    base = os.path.dirname(os.path.abspath(__file__))
    dll_path = os.path.abspath(os.path.join(base, "..", "libs", "linklist_teaching.dll"))
    if not os.path.exists(dll_path):
        # Windows 路径大小写可能无所谓；尝试 without .. as well
        # 也允许用户在环境变量中指定 LINKEDLIST_DLL
        env = os.environ.get("LINKEDLIST_DLL")
        if env and os.path.exists(env):
            dll_path = env
        else:
            _using_cpp = False
            _lib = None
            return
    try:
        _lib = ctypes.CDLL(dll_path)
        # 设置 argtypes/restype
        _lib.ll_create.restype = c_void_p
        _lib.ll_destroy.argtypes = [c_void_p]

        _lib.ll_insert_head.argtypes = [c_void_p, c_int]
        _lib.ll_insert_tail.argtypes = [c_void_p, c_int]
        _lib.ll_insert_at.argtypes = [c_void_p, c_int, c_int]

        _lib.ll_delete_value.argtypes = [c_void_p, c_int]
        _lib.ll_delete_at.argtypes = [c_void_p, c_int]

        _lib.ll_reverse.argtypes = [c_void_p]
        _lib.ll_search.argtypes = [c_void_p, c_int]
        _lib.ll_size.argtypes = [c_void_p]

        _lib.ll_to_array.argtypes = [c_void_p, ctypes.POINTER(c_int)]
        _lib.ll_to_array.restype = POINTER(c_int)
        _lib.ll_free_array.argtypes = [POINTER(c_int)]

        _using_cpp = True
    except Exception as e:
        # 加载失败时回退到 Python 实现
        _lib = None
        _using_cpp = False

# 立即尝试加载 DLL（如果存在）
_load_dll()

def _new_id() -> str:
    return uuid.uuid4().hex

def create_list(initial: Optional[List[int]] = None) -> str:
    """
    创建一个链表，返回 id（字符串 UUID）。
    initial: 可选的整数列表，用于初始化节点（按顺序插入 tail）。
    """
    with _lock:
        lid = _new_id()
        if _using_cpp and _lib:
            h = _lib.ll_create()
            if not h:
                # fallback to python
                inst = LinkedListPY()
                _lists[lid] = ("py", inst)
            else:
                _lists[lid] = ("c", c_void_p(h))
                if initial:
                    for v in initial:
                        _lib.ll_insert_tail(_lists[lid][1], int(v))
        else:
            inst = LinkedListPY()
            if initial:
                for v in initial:
                    inst.insert_tail(int(v))
            _lists[lid] = ("py", inst)
        return lid

def destroy_list(lid: str) -> bool:
    with _lock:
        info = _lists.pop(lid, None)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            _lib.ll_destroy(val)
        # python instance simply garbage-collected
        return True

# 操作封装（insert_head, insert_tail, insert_at, delete_value, delete_at, reverse, search, size, to_list）
def insert_head(lid: str, value: int) -> bool:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            res = _lib.ll_insert_head(val, int(value))
            return res == 0
        else:
            val.insert_head(int(value))
            return True

def insert_tail(lid: str, value: int) -> bool:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            res = _lib.ll_insert_tail(val, int(value))
            return res == 0
        else:
            val.insert_tail(int(value))
            return True

def insert_at(lid: str, index: int, value: int) -> bool:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            res = _lib.ll_insert_at(val, int(index), int(value))
            return res == 0
        else:
            return val.insert_at(int(index), int(value))

def delete_value(lid: str, value: int) -> int:
    """
    删除第一个匹配的值，返回 1 表示删除成功，0 未找到，-1 表示错误
    """
    with _lock:
        info = _lists.get(lid)
        if not info:
            return -1
        kind, val = info
        if kind == "c" and _lib:
            return int(_lib.ll_delete_value(val, int(value)))
        else:
            return int(val.delete_value(int(value)))

def delete_at(lid: str, index: int) -> bool:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            return _lib.ll_delete_at(val, int(index)) == 0
        else:
            return val.delete_at(int(index))

def reverse(lid: str) -> bool:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return False
        kind, val = info
        if kind == "c" and _lib:
            return _lib.ll_reverse(val) == 0
        else:
            val.reverse()
            return True

def search(lid: str, value: int) -> int:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return -1
        kind, val = info
        if kind == "c" and _lib:
            return int(_lib.ll_search(val, int(value)))
        else:
            return int(val.search(int(value)))

def size(lid: str) -> int:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return -1
        kind, val = info
        if kind == "c" and _lib:
            return int(_lib.ll_size(val))
        else:
            return int(val.size())

def to_list(lid: str) -> Optional[List[int]]:
    with _lock:
        info = _lists.get(lid)
        if not info:
            return None
        kind, val = info
        if kind == "c" and _lib:
            out_len = c_int()
            arr_ptr = _lib.ll_to_array(val, ctypes.byref(out_len))
            if not arr_ptr:
                return []
            length = int(out_len.value)
            pylist = [int(arr_ptr[i]) for i in range(length)]
            # 释放 C 分配的内存
            _lib.ll_free_array(arr_ptr)
            return pylist
        else:
            return val.to_list()

# 额外的 helper：列出当前管理的 id
def list_ids():
    with _lock:
        return list(_lists.keys())

# 暴露是否使用 C++ 后端
def using_cpp_backend() -> bool:
    return _using_cpp and (_lib is not None)
