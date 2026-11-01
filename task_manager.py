import json
import os

FILE_PATH="tasks.json"

def load_tasks():
    if not os.path.exists(FILE_PATH):
        return[]
    with open(FILE_PATH,"r",encoding="utf-8") as f:
        return json.load(f)

def save_tasks():
    with open(FILE_PATH,"w",encoding="utf-8") as f:
        json.dump(tasks,f,ensure_ascii=False,indent=4)

tasks=load_tasks()

def add_task(name, hours):
    """添加一项学习任务"""
    if not name.strip():
        return "任务名称不能为空"

    if hours <= 0:
        return "学习时长必须大于0"

    task = {
        "name": name,
        "hours": hours
    }

    tasks.append(task)
    save_tasks()
    return f"任务添加成功：{name}"


def list_tasks():
    """查询全部学习任务"""
    if not tasks:
        return "当前没有学习任务"

    lines = []

    for index, task in enumerate(tasks, start=1):
        lines.append(
            f"{index}. {task['name']}：{task['hours']}小时"
        )

    return "\n".join(lines)


def total_task_hours():
    """计算所有学习任务的总时长"""
    total = 0

    for task in tasks:
        total += task["hours"]

    return total
