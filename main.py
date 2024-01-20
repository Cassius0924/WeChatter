# 项目启动文件
import uvicorn
from bot_info import BotInfo
from config.config_reader import ConfigReader
from utils.file_manager import FileManager
from sqlite.sqlite_manager import SqliteManager

# 启动命令：python main.py

cr = ConfigReader("config.ini")


def main():
    BotInfo.update_name(cr.bot_name)
    # 检查数据文件夹是否存在，不存在则创建
    FileManager.check_and_create_folder("data/qrcodes")
    FileManager.check_and_create_folder("data/todos")
    # FileManager.check_and_create_folder("data/copilot_gpt4/chats")

    sqlite_manager = SqliteManager("data/wechatbot.sqlite")
    # sqlite_manager.check_and_create_table("wx_users", ["id INTEGER PRIMARY KEY", "chat TEXT"])
    # sqlite_manager.check_and_create_table("copilot_chats", ["id INTEGER PRIMARY KEY", "chat TEXT"])
    # sqlite_manager.check_and_create_table("chat_conversations", ["id INTEGER PRIMARY KEY", "chat TEXT"])

    from recv_msg import app

    uvicorn.run(app, host="0.0.0.0", port=cr.recv_port)


if __name__ == "__main__":
    main()
