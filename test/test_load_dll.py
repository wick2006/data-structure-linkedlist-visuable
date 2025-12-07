import ctypes, os

dll_path = r"C:\Users\l\Desktop\华南师范大学\作业\大二上\数据结构实验\project1\libs\linklist_teaching.dll"

print("DLL exists:", os.path.exists(dll_path))
print("Trying to load…")

try:
    lib = ctypes.CDLL(dll_path)
    print("DLL loaded successfully!")
except OSError as e:
    print("Load failed:", e)
