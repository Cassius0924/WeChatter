# ⚙️ 自定义命令关键词配置详细

本篇文档仅包含配置文件中自定义命令关键词配置的详细说明，更多配置请查看项目[自述文件](../README.md#配置文件)

## 所有命令名称

- `help`: 查看命令帮助
- `weather`: 查询天气预报
- `weibo-hot`: 获取微博热搜
- `zhihu-hot`: 获取知乎热搜
- `bili-hot`: 获取 Bilibili 热搜
- `douyin-hot`: 获取抖音热搜
- `word`: 单词/词语翻译
- People Daily
  - `people-daily`: 获取人民日报 PDF
  - `people-daily-url`: 获取人民日报 URL
- TODO
  - `todo`: 添加待办事项
  - `todo-remove`: 删除待办事项
- `food-calories`: 获取食物热量
- `today-in-history`: 获取历史上的今天
- `github-trending`: 获取 GitHub 趋势
- `qrcode`: 生成二维码
- `pai-post`: 获取少数派早报
- GPT3.5
  - `gpt`: 继续 GPT3.5 问答
  - `gpt-chats`: 查看 GPT3.5 对话
  - `gpt-record`: 查看 GPT3.5 记录
  - `gpt-continue`: 继续 GPT3.5 继续
- GPT4
  - `gpt4`: 进行 GPT4 问答
  - `gpt4-chats`: 查看 GPT4 对话记录
  - `gpt4-record`: 查看 GPT4 聊天记录
  - `gpt4-continue`: 继续 GPT4 对话

## 自定义命令关键词配置

- **[示例一]** 为 `gpt4` 命令添加自定义命令关键词 `>`，为 `weather` 命令添加自定义命令关键词 `tq`, `气温`

  ```ini
  custom_command_key_dict = {
            "gpt4": [">"],
            "weather": ["tq", "气温"]
          }
  ```
