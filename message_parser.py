from command.gpt_reply import reply_by_gpt35, reply_by_gpt4
from send_msg import send_text_msg, reply_over, send_file_msg, send_image_msg
from command.bili_hot import get_bili_hot_str
from command.command_set import cmd_dict


class MessageParser:
    def __init__(self) -> None:
        pass

    def parse_message(self, message: str, to_user_name: str):
        message, desc_and_cmd = self.__parse_command(message)
        desc, cmd = desc_and_cmd["desc"], desc_and_cmd["value"]
        print(desc)
        # 非命令消息
        if cmd == 0:
            print("该消息不是命令类型")
            return 
        # 是命令消息
        reply_over(to_user_name)
        if cmd == self.__get_cmd_value("gpt4"):
            send_text_msg(reply_by_gpt4(message), to_user_name)
        elif cmd == self.__get_cmd_value("gpt"):
            send_text_msg(reply_by_gpt35(message), to_user_name)
        elif cmd == self.__get_cmd_value("bili-hot"):
            send_text_msg(get_bili_hot_str(), to_user_name)
        elif cmd == self.__get_cmd_value("help"):
            send_text_msg(self.__get_help_msg(), to_user_name)

    def __parse_command(self, message: str) -> int:
        for value in cmd_dict.values():
            for key in value["keys"]:
                if message.startswith("/" + key):
                    message = message[len(key) + 1:]
                    return message, {"desc": value["desc"], "value": value["value"]}
        return message, {"desc": cmd_dict["None"]["desc"], "value": cmd_dict["None"]["value"]}

    def __get_cmd_value(self, cmd: str) -> int:
        return cmd_dict[cmd]["value"]

    def __get_help_msg(self):
        help_msg = "=====帮助信息=====\n"
        for value in cmd_dict.values():
            if value["value"] == 0:
                continue
            help_msg += "/" + value["keys"][0] + ": " + value["desc"] + "\n"
        return help_msg
