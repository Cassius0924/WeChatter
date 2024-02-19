# WeChatter 启动文件
import uvicorn
from loguru import logger

import wechatter.database as db
import wechatter.utils.file_manager as fm
from wechatter.init_logger import init_logger


def main():
    # 初始化 logger
    init_logger()

    # isort: off
    # 在初始化 logger 之后导入 config 模块
    from wechatter.config import config

    # 为了让此文件的 config 模块是首次导入，下面这些模块需要放到 config 导入之后
    from wechatter.app.app import app
    from wechatter.bot.bot_info import BotInfo
    # isort: on

    BotInfo.update_name(config.bot_name)
    # 创建文件夹
    fm.check_and_create_folder("data/qrcodes")
    fm.check_and_create_folder("data/todos")
    fm.check_and_create_folder("data/text_image")

    db.create_tables()

    logger.info("WeChatter 启动成功！")
    # 启动uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.wechatter_port)


if __name__ == "__main__":
    main()
