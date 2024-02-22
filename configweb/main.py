import logging
import subprocess
import threading

from fastapi import Body
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from ruamel.yaml import YAML
from ruamel.yaml.comments import CommentedSeq

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


def get_config_sections(section_names):
    try:
        yaml = YAML()
        with open('../config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f)
        section_configs = {section_name: config.get(section_name) for section_name in section_names}
        for section_name, section_config in section_configs.items():
            print(f"!!!{config.get(section_name)}type:{type(config.get(section_name))}!!!")
            if section_config is None:
                raise KeyError(f"Section '{section_name}' not found in configuration file.")
        return section_configs
    except Exception as e:
        return {"error": str(e)}


def update_config_section(section_name, updated_value):
    try:
        yaml = YAML()
        yaml.preserve_quotes = True
        yaml.indent(mapping=2, sequence=4, offset=2)

        # 先读取整个配置文件
        with open('../config.yaml', 'r', encoding='utf-8') as f:
            config = yaml.load(f)
        old_value = config.get(section_name)
        new_value = updated_value.get(section_name)

        print(f"旧值是 {old_value}")
        print(f"新值是 {new_value}")

        # 判断old_value是什么类型
        print(f"旧值的类型是{type(old_value)}")
        # 判断new_value是什么类型
        print(f"更新前，新值的类型是{type(new_value)}")

        # 判断新旧两个值是否相同
        if old_value == new_value:
            print(f"新旧两个值相同，无需更新: {section_name} : (old:{old_value} --> new:{new_value})")
            return {"message": "新旧两个值相同，无需更新", "changes": {section_name: (old_value, new_value)}}
        # 判断新旧两个值的类型是否相同
        # if type(old_value) != type(new_value):
        if not isinstance(old_value, type(new_value)):
            if isinstance(old_value, int) and isinstance(new_value,
                                                         str):  # 情况1：旧值是int，新值是str（前端传过来的是str）如（wechatter_port）
                if new_value.isdigit():
                    new_value = int(new_value)
                    print(f"更新前，新值是str，转换为int: {new_value}")
                else:
                    pass
            elif isinstance(old_value, bool) and isinstance(new_value,
                                                            str):  # 情况2：旧值是bool，新值是str，如（need_mentioned
                # 、github_webhook_enabled、message_forwarding_enabled、all_task_cron_enabled）
                if new_value.lower() == 'true':
                    new_value = True
                    print(f"更新前，新值是str，转换为bool: {new_value}")
                elif new_value.lower() == 'false':
                    new_value = False
                    print(f"更新前，新值是str，转换为bool: {new_value}")
                else:
                    raise ValueError(f"请输入正确的bool值: {new_value}")
            elif isinstance(old_value, CommentedSeq) and isinstance(new_value,
                                                                    str):  # 情况3：旧值是ruamel.yaml
                # .comments.CommentedSeq，新值是str，如（admin_list,admin_group_list,）
                value = new_value.split(',')
                new_value = CommentedSeq(value)
                print(f"更新前，新值是str，转换为CommentedSeq: {new_value}")
            elif isinstance(old_value, CommentedSeq) and isinstance(new_value,
                                                                    list):  # 情况4：旧值是ruamel.yaml.comments.CommentedSeq，新值是list，如（message_forwarding_rule_list）
                # 遍历列表中的每个字典
                for dict_obj in new_value:
                    # 遍历字典中的每个键和值
                    for key, value in dict_obj.items():
                        # 检查值是否是字符串
                        if isinstance(value, str):
                            # 如果是，尝试将其分割为列表
                            dict_obj[key] = value.split(',')

                new_value = CommentedSeq(new_value)
                print(f"更新前，新值是list，转换为CommentedSeq: {new_value}")
            else:
                pass

        # 写入配置文件
        print(f"更新后，新的type是{type(new_value)}")
        config[section_name] = new_value
        print(config[section_name])
        with open('../config.yaml', 'w', encoding='utf-8') as f:
            yaml.dump(config, f)
            print(f"Config updated successfully: {section_name} : (old:{old_value} --> new:{new_value})")
            return {"message": "Config updated successfully", "changes": {section_name: (old_value, new_value)}}
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
    sections = get_config_sections(['wechatter_port'])
    return sections


@app.post("/wechatter")
def update_wechatter_config(updated_config: dict = Body(...)):
    succeed_wechatter_port = update_config_section('wechatter_port', updated_config)
    return {"wechatter_port": succeed_wechatter_port}


@app.get("/wx-bot-webhook")
def get_wx_bot_webhook_config():
    sections = get_config_sections(['wx_webhook_base_api', 'wx_webhook_recv_api_path'])
    return sections


@app.post("/wx-bot-webhook")
def update_wx_bot_webhook_config(updated_config: dict = Body(...)):
    succeed_wx_webhook_base_api = update_config_section('wx_webhook_base_api', updated_config)
    succeed_wx_webhook_recv_api_path = update_config_section('wx_webhook_recv_api_path', updated_config)
    return {"wx_webhook_base_api": succeed_wx_webhook_base_api,
            "wx_webhook_recv_api_path": succeed_wx_webhook_recv_api_path}


@app.get("/admin")
def get_admin_config():
    sections = get_config_sections(['admin_list', 'admin_group_list'])
    return sections


@app.post("/admin")
def update_admin_config(updated_config: dict = Body(...)):
    succeed_admin_list = update_config_section('admin_list', updated_config)
    succeed_admin_group_list = update_config_section('admin_group_list', updated_config)
    return {"admin_list": succeed_admin_list, "admin_group_list": succeed_admin_group_list}


@app.get("/bot")
def get_bot_config():
    sections = get_config_sections(['bot_name'])
    return sections


@app.post("/bot")
def update_bot_config(updated_config: dict = Body(...)):
    succeed_bot_name = update_config_section('bot_name', updated_config)
    return {"bot_name": succeed_bot_name}


@app.get("/chat")
def get_chat_config():
    sections = get_config_sections(['command_prefix', 'need_mentioned'])
    return sections


@app.post("/chat")
def update_chat_config(updated_config: dict = Body(...)):
    succeed_command_prefix = update_config_section('command_prefix', updated_config)
    succeed_need_mentioned = update_config_section('need_mentioned', updated_config)
    return {"command_prefix": succeed_command_prefix, "need_mentioned": succeed_need_mentioned}


@app.get("/copilot-gpt4")
def get_copilot_gpt4_config():
    sections = get_config_sections(['cp_gpt4_base_api', 'cp_token'])
    return sections


@app.post("/copilot-gpt4")
def update_copilot_gpt4_config(updated_config: dict = Body(...)):
    succeed_cp_gpt4_base_api = update_config_section('cp_gpt4_base_api', updated_config)
    succeed_cp_token = update_config_section('cp_token', updated_config)
    return {"cp_gpt4_base_api": succeed_cp_gpt4_base_api, "cp_token": succeed_cp_token}


@app.get("/github-webhook")
def get_github_webhook_config():
    sections = get_config_sections(
        ['github_webhook_enabled', 'github_webhook_api_path', 'github_webhook_receive_person_list',
         'github_webhook_receive_group_list'])
    return sections


@app.post("/github-webhook")
def update_github_webhook_config(updated_config: dict = Body(...)):
    succeed_github_webhook_enabled = update_config_section('github_webhook_enabled', updated_config)
    succeed_github_webhook_api_path = update_config_section('github_webhook_api_path', updated_config)
    succeed_github_webhook_receive_person_list = update_config_section('github_webhook_receive_person_list',
                                                                       updated_config)
    succeed_github_webhook_receive_group_list = update_config_section('github_webhook_receive_group_list',
                                                                      updated_config)
    return {"github_webhook_enabled": succeed_github_webhook_enabled,
            "github_webhook_api_path": succeed_github_webhook_api_path,
            "github_webhook_receive_person_list": succeed_github_webhook_receive_person_list,
            "github_webhook_receive_group_list": succeed_github_webhook_receive_group_list}


@app.get("/message-forwarding")
def get_message_forwarding_config():
    sections = get_config_sections(['message_forwarding_enabled', 'message_forwarding_rule_list'])
    return sections


@app.post("/message-forwarding")
def update_message_forwarding_config(updated_config: dict = Body(...)):
    succeed_message_forwarding_enabled = update_config_section('message_forwarding_enabled', updated_config)
    succeed_message_forwarding_rule_list = update_config_section('message_forwarding_rule_list', updated_config)
    return {"message_forwarding_enabled": succeed_message_forwarding_enabled,
            "message_forwarding_rule_list": succeed_message_forwarding_rule_list}


@app.get("/task-cron")
def get_task_cron_config():
    sections = get_config_sections(['all_task_cron_enabled', 'task_cron_list'])
    return sections


@app.post("/task-cron")
def update_task_cron_config(updated_config: dict = Body(...)):
    succeed_all_task_cron_enabled = update_config_section('all_task_cron_enabled', updated_config)
    succeed_task_cron_list = update_config_section('task_cron_list', updated_config)
    return {"all_task_cron_enabled": succeed_all_task_cron_enabled, "task_cron_list": succeed_task_cron_list}


@app.get("/custom-command-key")
def get_custom_command_key_config():
    sections = get_config_sections(['custom_command_key_dict'])
    return sections


@app.post("/custom-command-key")
def update_custom_command_key_config(updated_config: dict = Body(...)):
    succeed_custom_command_key_dict = update_config_section('custom_command_key_dict', updated_config)
    return {"custom_command_key_dict": succeed_custom_command_key_dict}


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
