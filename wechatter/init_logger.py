import logging
import os
import sys

from loguru import logger

from wechatter.utils.path_manager import get_abs_path

# 使用环境变量中的 LOG_LEVEL
LOG_LEVEL_NAME = os.environ.get("WECHATTER_LOG_LEVEL", "INFO")
LOG_LEVEL = logging.getLevelName(LOG_LEVEL_NAME)

LOGURU_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <3}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

LOG_FILE = get_abs_path("logs/wechatter_{time:YYYY-MM-DD}.log")


# 将 FastAPI 的日志记录到 Loguru 中
class InterceptHandler(logging.Handler):
    def emit(self, record):
        # 获取对应的 Loguru 级别（如果存在）
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        # 查找记录消息的调用者
        frame, depth = sys._getframe(6), 6
        while frame and frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )
        # TODO: 解决DEBUG级别下multipart.multipart:callback太多问题


def init_logger(log_level: str = ""):
    if log_level:
        global LOG_LEVEL_NAME, LOG_LEVEL
        LOG_LEVEL_NAME = log_level
        LOG_LEVEL = logging.getLevelName(LOG_LEVEL_NAME)

    # 拦截根日志记录器的所有内容
    logging.root.handlers = [InterceptHandler()]
    logging.root.setLevel(LOG_LEVEL)

    # 删除其他日志记录器的处理程序并传播到根日志记录器
    for name in logging.root.manager.loggerDict.keys():
        logging.getLogger(name).handlers = []
        logging.getLogger(name).propagate = True

    logger.configure(
        handlers=[
            {
                "sink": sys.stdout,
                "format": LOGURU_FORMAT,
                "level": LOG_LEVEL_NAME,
            }
        ],
    )

    # 添加日志文件
    logger.add(
        LOG_FILE,
        rotation="00:00",
        encoding="utf-8",
        format=LOGURU_FORMAT,
    )
