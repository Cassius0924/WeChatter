import uvicorn
from recv_msg import app

# 项目启动文件
# 启动命令：python main.py


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=400)
