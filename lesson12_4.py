import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# 读取环境变量
load_dotenv()

# 初始化 DeepSeek
client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 第一步：让大模型生成学习计划
def create_plan(user_goal, errors=None):

    messages = [
        {
            "role": "system",
            "content": """
你是一个学习计划规划助手。

请根据用户的学习目标制定计划。

必须严格遵守用户提出的时间限制。
请严格返回 JSON，不要添加 Markdown 代码块。

格式：
{
    "goal": "学习目标",
    "plan": [
        {
            "day": "第1天",
            "task": "具体学习任务",
            "hours": 1.5
        }
    ]
}
"""
        },
        {
            "role": "user",
            "content": user_goal
        }
    ]

    # 如果存在错误，把错误反馈给大模型
    if errors:
        messages.append({
            "role": "user",
            "content": f"""
上一次生成的计划没有通过 Python 验证。

存在以下错误：
{json.dumps(errors, ensure_ascii=False)}

请根据这些错误修改计划，重新生成完整的 JSON。
不要只返回修改的部分。
"""
        })

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    content = response.choices[0].message.content

    plan = json.loads(content)

    return plan


# 第二步：使用 Python 验证计划
def check_plan(plan, max_hours):

    errors = []

    for item in plan["plan"]:

        if item["hours"] > max_hours:

            errors.append(
                f"{item['day']}安排超时："
                f"{item['hours']}小时，"
                f"最多允许{max_hours}小时"
            )

    if errors:
        return False, errors

    return True, []


# 第三步：让 Agent 自动生成、验证和修正计划
def run_agent(user_goal, max_hours):

    max_retries = 3

    errors = []

    for attempt in range(max_retries + 1):

        print(f"\n正在生成计划，第{attempt + 1}次...")

        # 生成计划
        plan = create_plan(user_goal, errors)

        # 验证计划
        is_valid, errors = check_plan(plan, max_hours)

        if is_valid:

            print("\n计划验证通过！")

            print("\n学习目标：", plan["goal"])
            print("\n最终学习计划：")

            for item in plan["plan"]:
                print(
                    f"{item['day']}：{item['task']}，"
                    f"{item['hours']}小时"
                )

            return

        print("\n计划验证失败：")

        for error in errors:
            print(error)

        if attempt < max_retries:
            print("\n正在将错误反馈给大模型，请它重新规划...")

    print("\n已经达到最大重试次数，计划仍未通过验证。")
    print("请调整目标或时间限制后重新尝试。")


# 获取用户目标
goal = input("请告诉我你的学习目标：")

# 获取每天最多学习多少小时
max_hours = float(input("每天最多学习多少小时："))

# 启动 Agent
run_agent(goal, max_hours)
