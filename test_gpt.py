import g4f
from command.gpt_reply import gpt_reply_by_bing

# print(gpt_reply_by_bing("为什么地球会转"))

# print([
#     provider.__name__
#     for provider in g4f.Provider.__providers__
#     if provider.working
# ])

response = g4f.ChatCompletion.create(
    model="gpt-4",
    # provider=g4f.Provider.Bing,
    messages=[{"role": "user", "content": "C++友元函数是什么？"}],
    stream=True,
)

for message in response:
    print(message, end=" ")

