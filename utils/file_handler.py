import os,hashlib
from utils.loger_handler import logger
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader,TextLoader

def get_file_md5_hex(file_path: str) -> str:#获取文件的md5的16进制字符串
    if not os.path.exists(file_path):
        logger.error(f"[md5计算]文件不存在: {file_path}")
        return

    if not os.path.isfile(file_path):
        logger.error(f"[md5计算]路径不是文件: {file_path}")
        return

    md5_obj = hashlib.md5()
    chunk_size = 4096#分片，避免文件过大爆内存

    try:
        with open(file_path, "rb") as f:#rb是二进制读取
            while chunk := f.read(chunk_size):#chunk := f.read(chunk_size)是Python的赋值表达式，它是一个语法糖，相当于：
                md5_obj.update(chunk)
            return md5_obj.hexdigest()
    except Exception as e:
        logger.error(f"[md5计算]计算失败: {e}")
        return None


def listdir_with_allowed_type(path: str, allowed_types: tuple[str]):#返货文件夹内的文件列表(允许的文件后缀)
    files = []

    if not os.path.isdir(path):
        logger.error(f"[文件列表]路径不是文件夹: {path}")
        return []

    for f in os.listdir(path):
        if f.endswith(allowed_types):
            files.append(os.path.join(path, f))
    return list(files)
        


def pdf_loader(file_path: str, passwd: str = None) -> list[Document]:#pdf文件加载器
    loader = PyPDFLoader(file_path, password=passwd)
    docs = loader.load()
    return docs


def text_loader(file_path: str) -> list[Document]:#文本文件加载器
    loader = TextLoader(file_path, encoding = "utf-8")
    docs = loader.load()
    return docs