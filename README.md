MIT License

Copyright (c) 2025 WICK KO

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights   
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell    
copies of the Software, and to permit persons to whom the Software is      
furnished to do so, subject to the following conditions:                    

The above copyright notice and this permission notice shall be included in all  
copies or substantial portions of the Software.                               

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER       
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING       
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER          
DEALINGS IN THE SOFTWARE.




### 概览（Project Summary）

这是一个教学用的 单链表可视化系统，后端由 C++ 实现核心链表算法并编译为 Windows DLL，前端通过 Django 提供 Web UI（HTML/CSS/JS）进行交互与动画演示。Python 通过 ctypes 调用 DLL，也可以回退到 Python 原生实现以便开发或部署。

主要目标：
- 演示单链表的创建、插入（头/尾/指定位置）、删除（按值/按索引）、反转、搜索、导出为数组等基本操作；

- 在前端直观展示链表每一步的变化并支持操作回放/快照；

- 后端用 C++ 保证算法性能与教学性

### 功能清单（Features）

- 单链表核心操作（C++ DLL 提供）：create / destroy / insert_head / insert_tail / insert_at / delete_value / delete_at / reverse / search / size / to_array / free_array。

- Django + 前端：操作面板、可视化面板、日志区、操作快照。

- 回退机制：若 DLL 无法加载，系统自动使用 linklist_py/linked_list.py 的 Python 实现。

- 静态资源：templates/linklist/index.html、static/linklist/css/style.css、static/linklist/js/app.js。

- 可测试：包含 tests/ 目录（占位），并提供 test_load.py 示例用于验证 DLL 加载。

### 项目结构

project1/
├── linklist_cpp/
│   ├── linkedlist.cpp
│   ├── linkedlist.h
│   ├── exports.def
│   └── (可选) build_dll.bat
├── libs/
│   └── linklist_teaching.dll      # 必须放这个位置，供 cpp_bridge.py 加载
├── linklist_py/
│   ├── __init__.py
│   ├── settings.py
│   ├── wsgi.py
│   ├── urls.py
│   ├── views.py
│   ├── models.py
│   ├── linked_list.py             # Python 回退实现
│   └── cpp_bridge.py              # ctypes 桥接（加载 DLL 或回退）
├── templates/
│   └── linklist/index.html
├── static/
│   └── linklist/css/style.css
│   └── linklist/js/app.js
├── tests/
├── manage.py
├── requirements.txt
└── README.md


### 开发环境

- Python 3.12（ 64-bit，与编译 DLL 的位数一致）

- Django（Django>=4.2）

- 用于编译 DLL：mingw-w64（x86_64）

### 启动开发服务器

python manage.py runserver

打开 http://127.0.0.1:8000

### 项目说明

#### cpp_bridge.py

- 尝试用 ctypes.CDLL 加载 libs/linklist_teaching.dll；

- 如果加载成功，设置每个导出函数的 argtypes / restype；

- 如果加载失败，回退到 Python 实现（linked_list.py），保持 API 一致。

#### API 设置(views.py)

POST /linklist/api/create/ — body: { "initial": [1,2,3] } → 返回 { "id": "uuid", "list": [...] }

POST /linklist/api/destroy/ — body: { "id": "..." }

POST /linklist/api/insert_head/ — { "id": "...", "value": 5 }

POST /linklist/api/insert_tail/ — { "id": "...", "value": 5 }

POST /linklist/api/insert_at/ — { "id":"...", "index":1, "value": 5 }

POST /linklist/api/delete_value/ — { "id":"...", "value": 5 }

POST /linklist/api/delete_at/ — { "id":"...", "index": 2 }

POST /linklist/api/reverse/ — { "id":"..." }

GET /linklist/api/search/?id=...&value=... → { "index": 2 }

GET /linklist/api/snapshot/?id=... → { "list": [...] }