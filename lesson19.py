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


# 定义 Agent 可以使用的工具
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
        {
            "role": "user",
            "content": user_input
        }
    ]

    # 记录成功和失败的工具
    completed_steps = []
    failed_steps = []

    # 最大模型请求轮数
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

        # 2. 如果模型没有调用工具，直接回答
        if not message.tool_calls:
            print("\nAgent：", message.content)
            return

        # 3. 保存模型的工具调用消息
        messages.append(message.model_dump(exclude_none=True))

        # 4. 逐个执行模型要求的工具
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            print("\n模型选择的工具：", function_name)

            # 初始化当前工具的执行状态
            tool_status = {
                "name": function_name,
                "success": False,
                "summary": ""
            }

            try:
                arguments = json.loads(
                    tool_call.function.arguments
                )

                print("模型提供的参数：", arguments)

                # 根据工具名称选择 Python 函数
                if function_name == "create_plan":

                    goal = arguments.get("goal")
                    max_hours = arguments.get("max_hours")

                    # 检查学习目标是否合法
                    if not isinstance(goal, str) or not goal.strip():
                        result = "执行失败：学习目标不能为空"
                        tool_status["summary"] = result

                    # 检查每天的学习时长是否合法
                    elif (
                        isinstance(max_hours, bool)
                        or not isinstance(max_hours, (int, float))
                        or max_hours <= 0
                    ):
                        result = "执行失败：学习时长参数不合法"
                        tool_status["summary"] = result

                    else:
                        # 调用学习计划生成函数
                        tool_result = run_agent(goal, max_hours)

                        result = json.dumps(
                            tool_result,
                            ensure_ascii=False
                        )

                        # 根据工具实际返回结果判断是否成功
                        if (
                            isinstance(tool_result, dict)
                            and tool_result.get("success") is True
                        ):
                            tool_status["success"] = True
                            tool_status["summary"] = tool_result.get(
                                "message",
                                "学习计划生成成功"
                            )
                        else:
                            tool_status["summary"] = (
                                tool_result.get(
                                    "message",
                                    "学习计划生成失败"
                                )
                                if isinstance(tool_result, dict)
                                else "工具返回结果格式不正确"
                            )

                elif function_name == "view_plan":

                    # 读取之前保存的学习计划
                    plan = load_plan()

                    if plan is None:
                        result = "目前没有保存过学习计划。"
                        tool_status["summary"] = result

                    else:
                        result = json.dumps(
                            plan,
                            ensure_ascii=False
                        )

                        tool_status["success"] = True
                        tool_status["summary"] = "学习计划读取成功"

                else:
                    result = "执行失败：未知工具。"
                    tool_status["summary"] = result

            except Exception as e:
                result = f"工具执行失败：{str(e)}"
                tool_status["summary"] = result

            # 根据工具执行状态记录成功或失败
            if tool_status["success"]:
                completed_steps.append(tool_status)
            else:
                failed_steps.append(tool_status)

            # 5. 把工具执行结果交还给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

            print("工具执行结果：", result)

    # 6. 达到最大执行轮数后停止
    print("\nAgent：达到最大执行步数，任务停止。")

    if completed_steps:
        print("\n已经成功完成的工具：")
        for item in completed_steps:
            print(f"- {item['name']}：{item['summary']}")

    if failed_steps:
        print("\n执行失败的工具：")
        for item in failed_steps:
            print(f"- {item['name']}：{item['summary']}")


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
