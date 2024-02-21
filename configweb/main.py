import logging
import subprocess
import threading

import yaml
from fastapi import Body
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# #本地测试
# FRONTEND_IP = "localhost"
# BACKEND_PORT = "3000"
# 服务器前端
FRONTEND_IP = "47.92.99.199"
FRONTEND_PORT = "3000"

# 其他代码...
FRONTEND_URL = f"http://{FRONTEND_IP}:"
origins = [
    FRONTEND_URL + FRONTEND_PORT,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# def get_config_section(section_name):
#     try:
#         config = configparser.ConfigParser()
#         config.read('../config.ini', encoding='utf-8')
#         section_config = dict(config[section_name])
#         return section_config
#     except Exception as e:
#         return {"error": str(e)}


def get_config_section(section_name):
    try:
        with open('../config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        section_config = config.get(section_name)
        if section_config is None:
            raise KeyError(f"Section '{section_name}' not found in configuration file.")
        return {section_name: str(section_config)}
    except Exception as e:
        return {"error": str(e)}


def update_config_section(section_name, updated_value):
    try:
        # 先读取整个配置文件
        with open('../config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)

        # 更新特定的部分
        config[section_name] = updated_value[section_name]

        # 再写回文件
        with open('../config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f)

        print(f"Config updated successfully: {section_name} - {updated_value}")
        return {"message": "Config updated successfully", "changes": updated_value}

    except Exception as e:
        return {"error": str(e)}



# ！！！已解决！！！解决方法：在run_command中，将process.stdout.readline()改为process.communicate()，并且将while True改为while process.poll()
# is None， 原因：process.stdout.readline()是阻塞的，会一直等待子进程的输出，直到子进程结束，而process.communicate(
# )是非阻塞的，会立即返回子进程的输出，如果子进程没有输出，就返回空字符串，如果子进程结束了，就返回子进程的输出，所以process.communicate()不会阻塞，而process.poll(
# )是非阻塞的，会立即返回子进程的状态，如果子进程结束了，就返回子进程的状态，如果子进程没有结束，就返回None，所以while process.poll() is None不会阻塞，而while True会阻塞，所以将while
# True改为while process.poll() is None就不会死锁了

# 死锁问题，问题具体如下：（现在用npm start就可以让前后端启动，在前端APP.js中，点击启动的button会执行await axios.post(`http://${BACKEND_URL}:${
# BACKEND_PORT}/run-main`)，服务器就会执行python3 main.py以启动另一个项目，cpu是正常的。点击停止的button会执行await axios.post(`http://${
# BACKEND_URL}:${BACKEND_PORT}/stop-main`)，服务器就会执行kill -9 $(lsof -t
# -i:400)，也执行成功了，已经启动的那个另一个项目的进程停止了，但是出现了问题：后端突然占用很大的cpu，平均有140%的cpu，具体是在点击停止的button的过程中，INFO:     Started reloader
# process [2993425] using StatReload INFO:     Started server process [
# 2993434]，这个2993434进程，突然变得占用cpu很大，他的command是python3 -c from multiprocessing.spawn import spawn main;spawn main(
# tracker fd=5,pipe handle=7)--multiprocessing-fork）

# def run_command(command, working_directory):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
#     while True:
#         output = process.stdout.readline()
#         if output == '' and process.poll() is not None:
#             break
#         if output:
#             print(output.strip())
#     return process.poll()


def run_command(command, working_directory):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               cwd=working_directory)

    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print("输出:", output.decode('utf-8'))

        error_output = process.stderr.readline()
        if error_output:
            print("错误输出:", error_output.decode('utf-8'))

    rc = process.poll()
    return rc


# def run_command(command, working_directory):
#     process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
#     while process.poll() is None:
#         output = process.communicate()  # 返回一个元组，第一个元素是子进程的输出，第二个元素是子进程的错误输出
#         if output == '' and process.poll() is not None:
#             break
#         if output:
#             print("输出:")
#             print("None" if output[0] is None else output[0].decode('utf-8'))
#             print("错误输出:")
#             print('None' if output[1] is None else output[1].decode('utf-8'))
#     return process.poll()


@app.get("/")
def read_root():
    return {"Hello": "ConfigWeb"}


@app.get("/wechatter")
def get_wechatter_config():
    return get_config_section('wechatter_port')


@app.post("/wechatter")
def update_wechatter_config(updated_config: dict = Body(...)):
    return update_config_section('wechatter_port', updated_config)


@app.get("/wx-bot-webhook")
def get_wx_bot_webhook_config():
    return get_config_section('wx-bot-webhook')


@app.post("/wx-bot-webhook")
def update_wx_bot_webhook_config(updated_config: dict = Body(...)):
    return update_config_section('wx-bot-webhook', updated_config)


@app.get("/admin")
def get_admin_config():
    return get_config_section('admin')


@app.post("/admin")
def update_admin_config(updated_config: dict = Body(...)):
    return update_config_section('admin', updated_config)


@app.get("/bot")
def get_bot_config():
    return get_config_section('bot')


@app.post("/bot")
def update_bot_config(updated_config: dict = Body(...)):
    return update_config_section('bot', updated_config)


@app.get("/chat")
def get_chat_config():
    return get_config_section('chat')


@app.post("/chat")
def update_chat_config(updated_config: dict = Body(...)):
    return update_config_section('chat', updated_config)


@app.get("/copilot-gpt4")
def get_copilot_gpt4_config():
    return get_config_section('copilot-gpt4')


@app.post("/copilot-gpt4")
def update_copilot_gpt4_config(updated_config: dict = Body(...)):
    return update_config_section('copilot-gpt4', updated_config)


@app.get("/github-webhook")
def get_github_webhook_config():
    return get_config_section('github-webhook')


@app.post("/github-webhook")
def update_github_webhook_config(updated_config: dict = Body(...)):
    return update_config_section('github-webhook', updated_config)


@app.get("/message-forwarding")
def get_message_forwarding_config():
    return get_config_section('message-forwarding')


@app.post("/message-forwarding")
def update_message_forwarding_config(updated_config: dict = Body(...)):
    return update_config_section('message-forwarding', updated_config)


@app.get("/weather-cron")
def get_weather_cron_config():
    return get_config_section('weather-cron')


@app.post("/weather-cron")
def update_weather_cron_config(updated_config: dict = Body(...)):
    return update_config_section('weather-cron', updated_config)


@app.get("/custom-command-key")
def get_custom_command_key_config():
    return get_config_section('custom-command-key')


@app.post("/custom-command-key")
def update_custom_command_key_config(updated_config: dict = Body(...)):
    return update_config_section('custom-command-key', updated_config)


@app.get("/gasoline-price-cron")
def get_gasoline_price_cron_config():
    return get_config_section('gasoline-price-cron')


@app.post("/gasoline-price-cron")
def update_gasoline_price_cron_config(updated_config: dict = Body(...)):
    return update_config_section('gasoline-price-cron', updated_config)


run_main_thread = None


@app.post("/run-main")
def run_main():
    global run_main_thread
    try:
        # TODO:改启动命令，python3，有的人的是python
        run_main_command = "python3 -m wechatter"
        run_main_directory = "../"

        run_main_thread = threading.Thread(target=run_command, args=(run_main_command, run_main_directory), daemon=True)
        run_main_thread.start()
        print("wechatter started")
        run_main_thread.join()  # join()的作用是等待子线程结束，如果不加join()，主线程会立即结束，子线程会继续执行，所以加了join()，主线程会等待子线程结束，然后主线程才会结束

        return {"message": "wechatter started"}
    except Exception as e:
        return {"error": str(e)}


@app.get("/run-main")
def run_main_is_alive():
    global run_main_thread
    if run_main_thread and run_main_thread.is_alive():
        return {"message": "wechatter is running"}
    else:
        return {"message": "wechatter is not running"}


@app.post("/stop-main")
def stop_main():
    try:
        # TODO:改停止命令，改端口号，从config.ini中读取

        # kill wechatter process
        stop_main_command = "kill $(lsof -t -i:400)"
        stop_main_directory = "../"

        stop_main_thread = threading.Thread(target=run_command, args=(stop_main_command, stop_main_directory),
                                            daemon=True)
        stop_main_thread.start()
        stop_main_thread.join()  # !!!已解决!!!这里会死锁，解决方法：在run_command中，将process.stdout.readline()改为process.communicate()，并且将while True改为while process.poll() is None
        print("wechatter stopped")

        return {"message": "wechatter stopped"}
    except Exception as e:
        return {"error": str(e)}
