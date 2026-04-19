"""
这是一个日志文件
"""

import logging
from utils.path_tool import get_abs_path
import os
from datetime import datetime

#日志保存的根目录
LOG_ROOT = get_abs_path("logs")

#确保日志的目录存在
os.makedirs(LOG_ROOT, exist_ok=True)

"""
%(asctime)s	日志记录的时间	2024-01-15 14:30:25,123
%(name)s	日志记录器的名称	__main__ 或 my_module
%(levelname)s	日志级别	INFO, ERROR, DEBUG 等
%(filename)s	产生日志的文件名	main.py, robot.py
%(lineno)d	产生日志的行号	42, 128(注意是 d 表示整数）
%(message)s	实际的日志消息	"机器人启动成功"
"""
#日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s"
)

def get_logger(
    name: str = "agent",
    console_level: int = logging.INFO,
    file_level: int = logging.DEBUG,
    log_file = None
) -> logging.Logger:
    """
    获取日志记录器
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    #避免重复添加Handler
    if logger.handlers:
        return logger

    #控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(console_handler)

    #文件Handler
    if not log_file:
        log_file = os.path.join(LOG_ROOT, f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log")
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(file_level)
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)
    logger.addHandler(file_handler)

    return logger

#快捷获取日志管理器
logger = get_logger()



if __name__ == "__main__":
    logger.info("测试日志")
    logger.error("测试错误日志")
    logger.debug("测试调试日志")
    logger.warning("测试警告日志")
