#
#  __     __   ______   ______   __  __   ______   ______  ______  ______   ______
# /\ \  _ \ \ /\  ___\ /\  ___\ /\ \_\ \ /\  __ \ /\__  _\/\__  _\/\  ___\ /\  == \
# \ \ \/ ".\ \\ \  __\ \ \ \____\ \  __ \\ \  __ \\/_/\ \/\/_/\ \/\ \  __\ \ \  __<
#  \ \__/".~\_\\ \_____\\ \_____\\ \_\ \_\\ \_\ \_\  \ \_\   \ \_\ \ \_____\\ \_\ \_\
#   \/_/   \/_/ \/_____/ \/_____/ \/_/\/_/ \/_/\/_/   \/_/    \/_/  \/_____/ \/_/ /_/
#

import uvicorn

import wechatter.database as db
import wechatter.utils.file_manager as fm
from wechatter.app.app import app
from wechatter.bot import BotInfo
from wechatter.config import config


def main():
    """
    WeChatter 启动文件
    """

    BotInfo.update_name(config["bot_name"])
    # 创建文件夹
    fm.check_and_create_folder("data/qrcodes")
    fm.check_and_create_folder("data/todos")
    fm.check_and_create_folder("data/text_image")

    db.create_tables()

    # 启动uvicorn
    port = config["wechatter_port"]
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()
