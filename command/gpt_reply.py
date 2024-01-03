# GPT回复命令
import g4f
# from g4f.Provider import Bing

def reply_by_gpt4(message) -> str:
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_4,
            # provider=g4f.Provider.Bing,
            messages=[{"role": "user", "content": message}],
            # stream=True,
        )
    except Exception as e:
        print(e)
        return "调用gpt4失败"
    return response_to_str(response)


def reply_by_gpt35(message) -> str:
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": message}],
        )
    except Exception as e:
        print(e)
        return "调用gpt3.5失败"
    return response_to_str(response)


def response_to_str(response) -> str:
    str = ""
    for message in response:
        str += message
    return str
