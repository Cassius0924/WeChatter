from wechatter.init_logger import init_logger

from .config import load_config

# 初始化 logger
init_logger()
# 加载配置
config = load_config()

__all__ = ["config"]
