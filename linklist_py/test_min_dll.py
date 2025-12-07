import ctypes
dll = ctypes.CDLL(r"C:\Users\l\Desktop\华南师范大学\作业\大二上\数据结构实验\project1\linklist_cpp\minimal_test.dll")
print(dll.add_numbers(2,3))
