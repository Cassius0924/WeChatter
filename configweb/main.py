import configparser
import logging
import subprocess
import threading

from fastapi import Body
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

logging.basicConfig(level=logging.DEBUG)
app = FastAPI()

# #本地测试
# BASE_URL = "http://localhost:"
# PORT = "3000"
# 服务器
BASE_URL = "http://47.92.99.199:"
PORT = "3000"

# 其他代码...

origins = [
    BASE_URL + PORT,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_config_section(section_name):
    try:
        config = configparser.ConfigParser()
        config.read('../config.ini', encoding='utf-8')
        section_config = dict(config[section_name])
        return section_config
    except Exception as e:
        return {"error": str(e)}


def update_config_section(section_name, updated_config):
    try:
        config = configparser.ConfigParser()
        config.read('../config.ini', encoding='utf-8')
        changes = {}
        for key, value in updated_config.items():
            old_value = config.get(section_name, key) if config.has_option(section_name, key) else None
            if old_value != value:
                config.set(section_name, key, value)
                changes[key] = {"old": old_value, "new": value}
        with open('../config.ini', 'w', encoding='utf-8') as configfile:
            config.write(configfile)
            print(f"Config updated successfully: {section_name} - {changes}")
        return {"message": "Config updated successfully", "changes": changes}
    except Exception as e:
        return {"error": str(e)}


def run_command(command, working_directory):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, cwd=working_directory)
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    return process.poll()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/wechatter")
def get_wechatter_config():
    return get_config_section('wechatter')


@app.post("/wechatter")
def update_wechatter_config(updated_config: dict = Body(...)):
    return update_config_section('wechatter', updated_config)


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


@app.post("/run-main")
def run_main():
    try:
        # TODO:改启动命令，python3，有的人的是python
        run_main_command = "python3 main.py"
        run_main_directory = "../"

        run_main_thread = threading.Thread(target=run_command, args=(run_main_command, run_main_directory), daemon=True)
        run_main_thread.start()
        run_main_thread.join()

        return {"message": "Main started"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/stop-main")
def stop_main():
    try:
        # Kill all child processes
        stop_child_processes_command = "kill $(lsof -t -i:8000)"  # 后端端口号
        # Kill the main process
        stop_main_command = "kill $(lsof -t -i:400)"  # wechatter端口号
        stop_main_directory = "../"

        stop_child_processes_thread = threading.Thread(target=run_command,
                                                       args=(stop_child_processes_command, stop_main_directory),
                                                       daemon=True)
        stop_child_processes_thread.start()
        stop_child_processes_thread.join()

        stop_main_thread = threading.Thread(target=run_command, args=(stop_main_command, stop_main_directory),
                                            daemon=True)
        stop_main_thread.start()
        stop_main_thread.join()

        return {"message": "Main and all child processes stopped"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/stop-main")
def stop_main():
    try:
        # kill wechatter process
        stop_main_command = "kill $(lsof -t -i:400)"
        stop_main_directory = "../"

        stop_main_thread = threading.Thread(target=run_command, args=(stop_main_command, stop_main_directory),
                                            daemon=True)
        stop_main_thread.start()
        stop_main_thread.join()
        print("wechatter stopped")

        # kill frontend process
        stop_frontend_command = "kill $(lsof -t -i:3000)"
        stop_frontend_directory = "../"

        stop_frontend_thread = threading.Thread(target=run_command,
                                                args=(stop_frontend_command, stop_frontend_directory), daemon=True)
        stop_frontend_thread.start()
        stop_frontend_thread.join()
        print("frontend stopped")

        # kill backend process
        # stop_backend_command = "kill $(lsof -t -i:8000)"
        stop_backend_command = "for pid in $(lsof -t -i:8000); do pkill -9 -P $pid; done"
        stop_backend_directory = "../"

        stop_backend_thread = threading.Thread(target=run_command, args=(stop_backend_command, stop_backend_directory),
                                               daemon=True)
        stop_backend_thread.start()
        stop_backend_thread.join()
        print("backend stopped")

        # # activate backend and frontend
        # # 直接执行npm start：
        # backend_and_frontend_command = "npm start"
        # backend_and_frontend_directory = "/myproject/WeChatter/configweb"
        #
        # backend_and_frontend_thread = threading.Thread(target=run_command, args=(
        #     backend_and_frontend_command, backend_and_frontend_directory), daemon=True)
        # backend_and_frontend_thread.start()
        # backend_and_frontend_thread.join()
        # print("backend and frontend started")

        return {"message": ""}
    except Exception as e:
        return {"error": str(e)}

# 无法解决死锁问题，问题具体如下：（现在用npm start就可以让前后端启动，在前端APP.js中，点击启动的button会执行await axios.post(`http://${BASE_URL}:${PORT}/run-main`)，服务器就会执行python3 main.py以启动另一个项目，cpu是正常的。点击停止的button会执行await axios.post(`http://${BASE_URL}:${PORT}/stop-main`)，服务器就会执行kill -9 $(lsof -t -i:400)，也执行成功了，已经启动的那个另一个项目的进程停止了，但是出现了问题：后端突然占用很大的cpu，平均有140%的cpu，具体是在点击停止的button的过程中，INFO:     Started reloader process [2993425] using StatReload
# INFO:     Started server process [2993434]，这个2993434进程，突然变得占用cpu很大，他的command是python3 -c from multiprocessing.spawn import spawn main;spawn main(tracker fd=5,pipe handle=7)--multiprocessing-fork）

# @app.post("/stop-main")
# def stop_main():
#     try:
#         #TODO:改停止命令，改端口号，从config.ini中读取
#         # stop_main_command = "kill -9 $(lsof -t -i:400)"
#         stop_main_command = "kill $(lsof -t -i:400)"
#         stop_main_directory = "../"
#
#         stop_main_thread = threading.Thread(target=run_command, args=(stop_main_command, stop_main_directory), daemon=True)
#         stop_main_thread.start()
#         stop_main_thread.join()
#
#         return {"message": "Main stopped"}
#     except Exception as e:
#         return {"error": str(e)}
