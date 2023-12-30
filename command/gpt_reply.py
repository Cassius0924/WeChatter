import g4f
# from g4f.Provider import Bing


def reply_by_gpt4(message) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        # provider=g4f.Provider.Bing,
        messages=[{"role": "user", "content": message}],
        # stream=True,
    )
    return response_to_str(response)


def reply_by_gpt35(message) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_35_turbo,
        messages=[{"role": "user", "content": message}],
    )
    return response_to_str(response)


def response_to_str(response)->str:
    str = ""
    for message in response:
        str += message
    return str


