import logging
import os
import sys

from loguru import logger

# 使用环境变量中的 LOG_LEVEL
LOG_LEVEL = logging.getLevelName(os.environ.get("LOG_LEVEL", "INFO"))

LOGURU_FORMAT = (
    "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
    "<level>{level: <3}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

LOG_FILE = "logs/wechatter_{time:YYYY-MM-DD}.log"


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


def init_logger():
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
