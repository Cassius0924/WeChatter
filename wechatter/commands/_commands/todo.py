import json
import os
import re
from typing import List

from wechatter.commands.handlers import command
from wechatter.models.message import SendMessage, SendMessageType, SendTo
from wechatter.sender import Sender
from wechatter.utils.path_manager import PathManager as pm


# TODO: 使用SQLite进行数据持久化
@command(
    command="todo",
    keys=["待办事项", "待办", "todo"],
    desc="获取待办事项。",
    value=110,
)
def todo_command_handler(to: SendTo, message: str = "") -> None:
    # 判断是查询还是添加
    if message == "":
        # 获取待办事项
        result = view_todos(to.p_id, to.p_name)
        Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
    else:
        # 添加待办事项
        add_success = add_todo_task(to.p_id, message)
        if add_success:
            result = view_todos(to.p_id, to.p_name)
            Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))
        else:
            Sender.send_msg(to, SendMessage(SendMessageType.TEXT, "添加失败"))


@command(
    command="remove-todo",
    keys=["删除待办事项", "remove-todo", "rmtd"],
    desc="删除待办事项。",
    value=111,
)
def remove_todo_command_handler(to: SendTo, message: str = "") -> None:
    indices = [
        int(idx.strip()) - 1
        for idx in re.split(r"[\s,]+", message)
        if idx.strip().isdigit()
    ]
    if not indices:
        Sender.send_msg(
            to, SendMessage(SendMessageType.TEXT, "请输入有效数字来删除待办事项")
        )
        return

    remove_result = remove_todo_task(to.p_id, indices)
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, remove_result))
    result = view_todos(to.p_id, to.p_name)
    Sender.send_msg(to, SendMessage(SendMessageType.TEXT, result))


def _load_todos(person_id: str) -> List[str]:
    """加载特定用户的待办事项"""
    file_path = pm.get_abs_path(
        os.path.join("data", "todos", f"p{person_id}_todo.json")
    )
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def _save_todos(person_id: str, content: List[str]) -> None:
    """保存待办事项到特定用户的 JSON 文件中"""
    file_path = pm.get_abs_path(
        os.path.join("data", "todos", f"p{person_id}_todo.json")
    )
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(json.dumps(content, ensure_ascii=False))
    # 上面这样写入会导致中文变成 Unicode 编码，可以使用下面的方式写入
    # with open(file_path, "w", encoding="utf-8") as file:
    #     file.write(json.dumps(content, ensure_ascii=False))


def add_todo_task(person_id: str, task: str) -> bool:
    """向待办事项列表中添加任务，并返回添加是否成功的状态"""
    todos = _load_todos(person_id)
    todos.append(task)  # 直接在原始列表上添加任务
    try:
        _save_todos(person_id, todos)
        return True  # 添加成功，返回 True
    except Exception as e:
        print(f"Error adding task: {e}")
        return False  # 添加失败，返回 False


def remove_todo_task(person_id: str, task_indices: List[int]) -> str:
    """从待办事项列表中删除任务，并返回删除的任务"""
    todos = _load_todos(person_id)
    removed_tasks = []
    for task_index in sorted(task_indices, reverse=True):
        if 0 <= task_index < len(todos):
            removed_task = todos.pop(task_index)  # 删除对应索引的任务
            removed_tasks.append(removed_task)
        else:
            return "请输入有效数字来删除待办事项"

    try:
        _save_todos(person_id, todos)
    except Exception as e:
        print(f"Error removing task: {e}")
        # If saving fails, add the tasks back
        todos.extend(removed_tasks)
        _save_todos(person_id, todos)
        return "删除失败"

    successful_removals = "✅成功删除待办事项✅\n"
    successful_removals += "\n".join(
        f"{i + 1}. {task}" for i, task in enumerate(removed_tasks)
    )
    return successful_removals


def view_todos(person_id: str, person_name: str) -> str:
    """查看特定用户的所有待办事项"""
    todos = _load_todos(person_id)
    personname = person_name
    if todos:
        formatted_todos = f"✨{personname}的待办事项✨\n"
        formatted_todos += "\n".join(f"{i + 1}. {task}" for i, task in enumerate(todos))
        return formatted_todos
    else:
        return "没有待办事项。"
