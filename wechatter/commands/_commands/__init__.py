# 导入该文件夹下所有模块

import glob
import importlib
import os

# 获取commands目录下所有的.py文件
command_files = glob.glob(os.path.dirname(__file__) + "/*.py")

for file in command_files:
    # 获取文件名（不包括扩展名）
    module_name = os.path.basename(file)[:-3]
    # 跳过__init__.py文件
    if module_name == "__init__":
        continue
    # 动态导入模块
    importlib.import_module("." + module_name, __package__)
