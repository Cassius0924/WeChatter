import requests


# 发送消息：curl -X POST http://localhost:3001/webhook/msg
def send_text_msg(message: str, to_user_name: str):
    url = "http://localhost:3001/webhook/msg"
    headers = {"Content-Type": "application/json"}
    data = {"to": to_user_name, "type": "text", "content": message}
    response = requests.post(url, headers=headers, json=data)
    # print(response)
    # print(response.text)

def send_image_msg(image_path: str, to_user_name: str):
    pass

def send_file_msg(file_path: str, to_user_name: str):
    pass
