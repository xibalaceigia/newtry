"""
为整个工程和提供统一的绝对路径
"""

import os



def get_project_root() -> str:
    """获取工程所在根目录"""
    #当前文件路径
    current_file = os.path.abspath(__file__)

    #当前文件所在文件夹
    current_dir = os.path.dirname(current_file)

    #获取根目录
    project_root = os.path.dirname(current_dir)

    return project_root

def get_abs_path(relative_path: str) -> str:
    """获取相对路径的绝对路径"""
    project_root = get_project_root()#得到工程根目录
    return os.path.join(project_root, relative_path)#将工程根目录和相对路径拼接起来
