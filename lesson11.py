import json

tasks = [
    {"name": "学习 C++", "hours": 2},
    {"name": "复习 Python", "hours": 1}
]

# 将任务写入 JSON 文件
with open("tasks.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, ensure_ascii=False, indent=4)

print("任务保存成功！")