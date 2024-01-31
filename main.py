# 项目启动文件
import uvicorn

import wechatter.config as config
from wechatter.app.app import app
from wechatter.bot.bot_info import BotInfo
from wechatter.sqlite.sqlite_manager import SqliteManager
from wechatter.utils.file_manager import FileManager


def main():
    BotInfo.update_name(config.bot_name)
    # 创建文件夹
    FileManager.check_and_create_folder("data/qrcodes")
    FileManager.check_and_create_folder("data/todos")
    FileManager.check_and_create_folder("data/text_image")
    # 创建文件
    FileManager.check_and_create_file("data/wechatter.sqlite")
    # 创建数据库表
    sqlite_manager = SqliteManager("data/wechatter.sqlite")
    sqlite_manager.excute_folder("wechatter/sqlite/sqls")
    # 启动uvicorn
    uvicorn.run(app, host="0.0.0.0", port=config.wechatter_port)


if __name__ == "__main__":
    main()
