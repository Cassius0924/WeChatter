import requests


# 发送消息：curl -X POST http://localhost:3001/webhook/msg
def send_text_msg(message: str, to_user_name: str):
    url = "http://localhost:3001/webhook/msg"
    headers = {"Content-Type": "application/json"}
    data = {"to": to_user_name, "type": "text", "content": message}
    requests.post(url, headers=headers, json=data)
    # print(response.text)


def acknowledge(to_user_name):
    msg = "收到命令请求"
    send_text_msg(msg, to_user_name)



def send_image_msg(image_path: str, to_user_name: str):
    pass

def send_file_msg(file_path: str, to_user_name: str):
    pass
