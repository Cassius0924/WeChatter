# 项目启动文件
import uvicorn
from loguru import logger

import wechatter.config as config
import wechatter.utils.file_manager as fm
from wechatter.app.app import app
from wechatter.bot.bot_info import BotInfo
from wechatter.init_logger import init_logger
from wechatter.sqlite.sqlite_manager import SqliteManager


def main():
    BotInfo.update_name(config.bot_name)
    # 创建文件夹
    fm.check_and_create_folder("data/qrcodes")
    fm.check_and_create_folder("data/todos")
    fm.check_and_create_folder("data/text_image")
    # 创建文件
    fm.check_and_create_file("data/wechatter.sqlite")
    # 创建数据库表
    sqlite_manager = SqliteManager("data/wechatter.sqlite")
    sqlite_manager.excute_folder("wechatter/sqlite/sqls")
    # 日志文件
    # 将 FastAPI 的日志输出到文件中
    init_logger()
    logger.info("Wechatter 启动成功！")
    # 启动uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.wechatter_port)


if __name__ == "__main__":
    main()
