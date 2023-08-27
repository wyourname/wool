import atexit
import os
from setuptools import setup, Extension
from Cython.Build import cythonize


extensions = [
    Extension("aiokgyy_310_x86", ["aiokgyy.py"]),
]

# 注册退出处理程序以删除生成的.c文件
def cleanup():
    for ext in extensions:
        for source in ext.sources:
            if source.endswith('.py'):
                c_file = source[:-3] + '.c'
                if os.path.exists(c_file):
                    os.remove(c_file)

atexit.register(cleanup)

setup(
    ext_modules=cythonize(extensions)
)
# 重命名生成的共享库文件
for ext in extensions:
    old_name = ext.name + '.cpython-310-x86_64-linux-gnu.so'
    new_name = ext.name + '.so'
    if os.path.exists(old_name):
        os.rename(old_name, new_name)
