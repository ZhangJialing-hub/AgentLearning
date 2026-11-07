import os
from openai import OpenAI
from dotenv import load_dotenv

from lesson15_f import run_agent
from lesson17 import load_plan


# 1. 初始化 DeepSeek
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# 2. 让 LLM 判断用户意图
def classify_intent(user_input):

    messages = [
        {
            "role": "system",
            "content": """
你是一个用户意图识别助手。

根据用户输入，判断用户想执行什么操作。

你只能返回以下四个标签之一，不要添加其他内容：

create_plan：用户想生成、制定或创建学习计划。
view_plan：用户想查看、读取之前保存的学习计划。
exit：用户想退出程序、结束对话。
unknown：用户的意图不属于以上三种，或者无法判断。

例如：
用户：帮我制定一个7天的C++学习计划
返回：create_plan

用户：看看之前保存的计划
返回：view_plan

用户：我要退出
返回：exit

用户：今天天气怎么样
返回：unknown
"""
        },
        {
            "role": "user",
            "content": user_input
        }
    ]

    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    intent = response.choices[0].message.content.strip()

    # 3. Python 检查 LLM 返回的标签是否合法
    allowed_intents = [
        "create_plan",
        "view_plan",
        "exit",
        "unknown"
    ]

    if intent not in allowed_intents:
        return "unknown"

    return intent


# 4. Agent 主程序
def main():

    while True:

        user_input = input("\n请告诉我你想做什么：").strip()

        if not user_input:
            print("请输入你的需求！")
            continue

        try:
            intent = classify_intent(user_input)
        except Exception as e:
            print("意图识别失败：", e)
            continue

        print("识别出的用户意图：", intent)

        if intent == "create_plan":

            try:
                max_hours = float(
                    input("每天最多学习多少小时：")
                )
            except ValueError:
                print("请输入正确的数字！")
                continue

            if max_hours <= 0:
                print("每天学习时长必须大于0！")
                continue

            run_agent(user_input, max_hours)

        elif intent == "view_plan":

            load_plan()

        elif intent == "exit":

            print("Agent 已退出，再见！")
            break

        else:

            print("暂时无法处理这个需求，请尝试生成或查看学习计划。")


if __name__ == "__main__":
    main()
