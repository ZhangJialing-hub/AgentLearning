import json

# 从 JSON 文件中读取任务
with open("tasks.json", "r", encoding="utf-8") as f:
    tasks = json.load(f)

# 输出读取到的任务
print("读取成功！")
print(tasks)

# 遍历任务列表
print("\n我的学习任务：")

for task in tasks:
    print(f"{task['name']}：{task['hours']}小时")