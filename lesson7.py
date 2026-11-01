from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# 1. 读取 API Key
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


# 2. 定义 Python 工具
def calculate_hours(daily_hours, days):
    """计算连续学习的总时长"""
    return daily_hours * days


def calculate_pomodoro(total_hours):
    """计算完整番茄钟数量，每个番茄钟共30分钟"""
    total_minutes = total_hours * 60
    cycles = total_minutes // 30
    return int(cycles)


# 3. 创建工具注册表
available_tools = {
    "calculate_hours": calculate_hours,
    "calculate_pomodoro": calculate_pomodoro
}


# 4. 告诉模型有哪些工具
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate_hours",
            "description": "计算连续学习的总时长",
            "parameters": {
                "type": "object",
                "properties": {
                    "daily_hours": {
                        "type": "number",
                        "description": "每天学习的小时数"
                    },
                    "days": {
                        "type": "integer",
                        "description": "学习天数"
                    }
                },
                "required": ["daily_hours", "days"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_pomodoro",
            "description": "根据总学习时间计算完整番茄钟数量，每个番茄钟包含25分钟学习和5分钟休息",
            "parameters": {
                "type": "object",
                "properties": {
                    "total_hours": {
                        "type": "number",
                        "description": "总学习时间，单位为小时"
                    }
                },
                "required": ["total_hours"]
            }
        }
    }
]


# 5. 接收用户问题
question = input("请输入你的学习问题：").strip()

if not question:
    print("问题不能为空")
    raise SystemExit

messages = [
    {
        "role": "user",
        "content": question
    }
]


# 6. 请求模型判断是否需要调用工具
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=messages,
    tools=tools,
    tool_choice="auto"
)

message = response.choices[0].message


# 7. 执行工具调用
if message.tool_calls:

    # 将模型的工具调用请求加入对话历史
    messages.append(message.model_dump(exclude_none=True))

    for tool_call in message.tool_calls:
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # 根据名称查找工具
        function = available_tools.get(function_name)

        if function is None:
            result = f"错误：找不到工具 {function_name}"
        else:
            try:
                # 执行对应的 Python 函数
                result = function(**arguments)
            except (TypeError, ValueError, KeyError) as e:
                result = f"工具执行失败：{e}"

        print(f"工具名称：{function_name}")
        print(f"工具执行结果：{result}")

        # 把工具执行结果交还给模型
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": str(result)
        })

    # 8. 让模型根据工具结果生成最终回答
    final_response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    print("\n最终回答：")
    print(final_response.choices[0].message.content)

else:
    # 模型判断不需要调用工具，直接回答
    print("\n模型回答：")
    print(message.content)



