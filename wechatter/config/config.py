from loguru import logger

from wechatter.config.config_reader import ConfigReader

config_reader = ConfigReader(config_file="config.ini")
logger.info("开始读取配置文件...")

# wechatter 配置
wechatter_port = config_reader.getint("wechatter", "wechatter_port")

# wx-bot-webhook 配置
wx_webhook_host = config_reader.getstr("wx-bot-webhook", "wx_webhook_host")
wx_webhook_port = config_reader.getint("wx-bot-webhook", "wx_webhook_port")
wx_webhook_recv_api_path = config_reader.getstr(
    "wx-bot-webhook", "wx_webhook_recv_api_path"
)

# admin 配置
admin_list = config_reader.getlist("admin", "admin_list")
admin_group_list = config_reader.getlist("admin", "admin_group_list")

# bot 配置
bot_name = config_reader.getstr("bot", "bot_name")

# chat 配置
command_prefix = config_reader.getstr("chat", "command_prefix")
need_mentioned = config_reader.getbool("chat", "need_mentioned")

# copilot-gpt4 配置
cp_gpt4_api_host = config_reader.getstr("copilot-gpt4", "cp_gpt4_api_host")
cp_gpt4_port = config_reader.getint("copilot-gpt4", "cp_gpt4_port")
cp_token = config_reader.getstr("copilot-gpt4", "cp_token")

# github-webhook 配置
github_webhook_enabled = config_reader.getbool(
    "github-webhook", "github_webhook_enabled"
)
github_webhook_api_path = config_reader.getstr(
    "github-webhook", "github_webhook_api_path"
)
github_webhook_receiver_list = config_reader.getlist(
    "github-webhook", "github_webhook_receiver_list"
)
github_webhook_receive_group_list = config_reader.getlist(
    "github-webhook", "github_webhook_receive_group_list"
)

# message-forwarding 配置
message_forwarding_enabled = config_reader.getbool(
    "message-forwarding", "message_forwarding_enabled"
)
message_forwarding_rules = config_reader.getlist(
    "message-forwarding", "message_forwarding_rules"
)

# weather-cron 配置
weather_cron_enabled = config_reader.getbool("weather-cron", "weather_cron_enabled")
weather_cron_rules = config_reader.getlist("weather-cron", "weather_cron_rules")

# gasoline-price-cron 配置
gasoline_price_cron_enable = config_reader.getbool(
    "gasoline-price-cron", "gasoline_price_cron_enabled"
)
gasoline_price_cron_rules = config_reader.getlist("gasoline-price-cron", "cron_rules")


logger.info(config_reader.config_dict)

logger.info("配置文件读取完毕！")
