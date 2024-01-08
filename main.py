# 项目启动文件
import uvicorn
from bot_info import BotInfo
from config.config_reader import ConfigReader
from utils.folder_manager import FolderManager

# 启动命令：python main.py

# FIXME: 运行项目时，必须在项目文件夹下执行，否则会报错找不到配置文件
cr = ConfigReader("config.ini")

if __name__ == "__main__":
    BotInfo.update_name(cr.bot_name)
    # 检查数据文件夹是否存在，不存在则创建
    FolderManager.check_and_create("data/qrcodes")
    FolderManager.check_and_create("data/todos")
    from recv_msg import app

    uvicorn.run(app, host="0.0.0.0", port=cr.recv_port)
