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
    print("==" * 20)
    print(content)
    '''
    {
      "event": "login", // login | logout | error
      "user": { // 当前的用户信息，没有则为null
        "_events": {},
        "_eventsCount": 0,
        "id": "@xxxasdfsf",
        "payload": {
          "alias": "",
          "avatar": "",
          "friend": false,
          "gender": 1,
          "id": "@xxx",
          "name": "somebody",
          "phone": [],
          "star": false,
          "type": 1
        }
        "error": ''// js 报错的错误栈信息
      }
    }
    '''
    print(source)
    print(isMentioned)
    print(isSystemEvent)
    print("==" * 20)
    to_user_name = get_user_name(source)    # 获取发送者的名字
    print(to_user_name + ": " + content)    
    message_parser.parse_message(content, to_user_name) # 解析消息
    return content, source


def get_user_name(source_str: str) -> str:
    source_dict = json.loads(source_str)
    return source_dict["from"]["payload"]["name"]


# 登录：curl http://localhost:3001/login\?token\=1213abac
# 检测登录状态：curl http://localhost:3001/loginCheck\?token\=1213aba
# 发送消息：curl --location --request POST 'http://localhost:3001/webhook/msg' --header 'Content-Type: application/json' --data-raw '{ "to": "缘", "type": "text", "content": "你好" }'
