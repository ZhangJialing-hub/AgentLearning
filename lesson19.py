import os
import json

from openai import OpenAI
from dotenv import load_dotenv

from lesson15_f import run_agent
from lesson17 import load_plan


load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


tools = [
    {
        "type": "function",
        "function": {
            "name": "create_plan",
            "description": "根据用户目标生成学习计划",
            "parameters": {
                "type": "object",
                "properties": {
                    "goal": {
                        "type": "string",
                        "description": "用户的学习目标"
                    },
                    "max_hours": {
                        "type": "number",
                        "description": "每天最多学习多少小时"
                    }
                },
                "required": ["goal", "max_hours"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "view_plan",
            "description": "查看之前保存的学习计划",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]

def ask_agent(user_input):
    messages = [
        {
            "role": "system",
            "content": """你是一个学习计划助手。
根据用户需求选择合适的工具：
1. 用户想制定、生成学习计划时，调用 create_plan。
2. 用户想查看之前保存的计划时，调用 view_plan。
3. 如果用户没有提出这两种需求，不要调用工具，直接说明目前只能生成或查看学习计划。

调用 create_plan 时：
- goal 必须包含用户提出的学习目标和学习天数。
- max_hours 必须是用户提出的每天最大学习时长。
- 如果用户没有提供每天最大学习时长，不要猜测，先询问用户。
"""
        },
        {"role": "user", "content": user_input}
    ]

    # 最多允许模型进行 5 轮决策
    MAX_STEPS = 5

    for step in range(MAX_STEPS):

        print(f"\n--- Agent 第 {step + 1} 轮 ---")

        # 1. 请求模型进行判断
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # 2. 如果模型没有调用工具，说明它准备直接回答
        if not message.tool_calls:
            print("\nAgent：", message.content)
            return

        # 3. 把模型的工具调用消息保存到对话历史
        messages.append(message.model_dump(exclude_none=True))

        # 4. 逐个执行模型要求的工具
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            print("\n模型选择的工具：", function_name)

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("模型提供的参数：", arguments)

                # 根据工具名称选择 Python 函数
                if function_name == "create_plan":

                    goal = arguments.get("goal")
                    max_hours = arguments.get("max_hours")

                    if not isinstance(goal, str) or not goal.strip():
                        result = "执行失败：学习目标不能为空"

                    elif (
                        isinstance(max_hours, bool)
                        or not isinstance(max_hours, (int, float))
                        or max_hours <= 0
                    ):
                        result = "执行失败：学习时长参数不合法"

                    else:
                     tool_result = run_agent(goal, max_hours)

                     result = json.dumps(
                       tool_result,
                       ensure_ascii=False
                    )       
                elif function_name == "view_plan":

                    plan = load_plan()

                    if plan is None:
                        result = "目前没有保存过学习计划。"
                    else:
                        result = json.dumps(
                            plan,
                            ensure_ascii=False
                        )

                else:
                    result = "执行失败：未知工具。"

            except Exception as e:
                result = f"工具执行失败：{str(e)}"

            # 5. 把工具执行结果交还给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

            print("工具执行结果：", result)

    # 6. 如果循环执行完 5 轮仍未结束，强制停止
    print("\nAgent：达到最大执行步数，任务停止。")

def main():

    while True:

        user_input = input("\n你：").strip()

        if user_input in ["退出", "exit", "quit"]:
            print("Agent 已退出，再见！")
            break

        if not user_input:
            continue

        try:
            ask_agent(user_input)
        except Exception as e:
            print("运行出错：", e)


if __name__ == "__main__":
    main()