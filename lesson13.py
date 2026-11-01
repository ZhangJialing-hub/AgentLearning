
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


def create_plan(user_goal):
    messages = [
        {
            "role": "system",
            "content": """
你是一个学习计划规划助手。

用户会告诉你学习目标和时间限制。
你需要根据用户的要求制定合理的学习计划。

请严格按照 JSON 格式返回，不要添加 Markdown 代码块。

返回格式：
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

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    # 获取大模型返回的内容
    content = response.choices[0].message.content

    # 将 JSON 字符串转换为 Python 字典
    plan = json.loads(content)

    return plan


# 获取用户目标
goal = input("请告诉我你的学习目标：")

# 让大模型制定计划
result = create_plan(goal)

# 输出计划
print("\n学习目标：", result["goal"])
print("\n制定的学习计划：")

for item in result["plan"]:
    print(
        f"{item['day']}：{item['task']}，"
        f"{item['hours']}小时"
    )
