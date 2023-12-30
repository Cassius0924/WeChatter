import uvicorn

from fastapi import FastAPI, Form
from message_parser import MessageParser
import json

app = FastAPI()

message_parser = MessageParser()


@app.post("/receive_msg")
async def recv_msg(
    type: str = Form(),
    content: str = Form(),
    source: str = Form(),
    isMentioned: str = Form(),
    isSystemEvent: str = Form(),
):
    to_user_name = get_user_name(source)
    print(to_user_name + ": " + content)
    message_parser.parse_message(content, to_user_name)
    return content, source


def get_user_name(source_str: str) -> str:
    source_dict = json.loads(source_str)
    return source_dict["from"]["payload"]["name"]


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4000)


# 登录：curl http://localhost:3001/login\?token\=1213abac
# 检测登录状态：curl http://localhost:3001/loginCheck\?token\=1213aba
# 发送消息：curl --location --request POST 'http://localhost:3001/webhook/msg' --header 'Content-Type: application/json' --data-raw '{ "to": "缘", "type": "text", "content": "你好" }'
