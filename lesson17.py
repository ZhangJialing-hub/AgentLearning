
import json
import os


def load_plan():

    # 1. 判断文件是否存在
    if not os.path.exists("study_plan.json"):
        print("还没有保存过学习计划")
        return None

    # 2. 读取 JSON 文件
    with open("study_plan.json", "r", encoding="utf-8") as f:
        plan = json.load(f)

    # 3. 输出学习目标
    print("\n历史学习计划")
    print("学习目标：", plan["goal"])

    # 4. 遍历并输出每天的任务
    for item in plan["plan"]:
        print(
            f"{item['day']}：{item['task']}，"
            f"{item['hours']}小时"
        )

    return plan


if __name__ == "__main__":
    load_plan()
