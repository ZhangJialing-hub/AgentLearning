
from task_manager import add_task, list_tasks, total_task_hours

# 添加任务
print(add_task("学习 C++", 2))
print(add_task("复习 Python", 1))
print(add_task("完成 Agent 项目", 3))

# 查询任务
print("\n我的学习任务：")
print(list_tasks())

# 统计总时长
print("\n总学习时长：", total_task_hours(), "小时")
