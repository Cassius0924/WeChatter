# GPT回复命令
import g4f


def reply_by_g4f_gpt4(message: str) -> str:
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
    return _response_to_str(response)


def reply_by_g4f_gpt35(message: str) -> str:
    """使用GPT3.5回复"""
    try:
        response = g4f.ChatCompletion.create(
            model=g4f.models.gpt_35_turbo,
            messages=[{"role": "user", "content": message}],
        )
    except Exception as e:
        print(e)
        return "调用gpt3.5失败"
    return _response_to_str(response)


def _response_to_str(response) -> str:
    str = ""
    for message in response:
        str += message
    return str
