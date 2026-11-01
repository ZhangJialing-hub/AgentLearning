
from openai import OpenAI
from dotenv import load_dotenv
import os
import json

# 导入之前写好的任务管理函数
from task_manager import add_task, list_tasks, total_task_hours


# 1. 初始化 DeepSeek
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)


# 2. 创建工具注册表
available_tools = {
    "add_task": add_task,
    "list_tasks": list_tasks,
    "total_task_hours": total_task_hours
}


# 3. 定义工具说明书
tools = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "添加一项学习任务",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "学习任务的名称"
                    },
                    "hours": {
                        "type": "number",
                        "description": "任务预计需要的学习小时数"
                    }
                },
                "required": ["name", "hours"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "查询当前所有学习任务",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "total_task_hours",
            "description": "计算当前所有学习任务的总学习时长",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


# 4. 创建对话历史
messages = [
    {
        "role": "system",
        "content": (
            "你是一个校园学习助手。"
            "你可以帮助用户添加学习任务、查询任务和统计总学习时长。"
            "涉及任务数据时，必须调用对应工具，不要编造执行结果。"
            "根据工具返回的结果向用户解释。"
        )
    }
]


# 5. 进入对话循环
print("校园学习助手已启动！输入 exit 退出。")

while True:

    question = input("\n你：").strip()

    if question.lower() == "exit":
        print("助手已退出。")
        break

    if not question:
        print("请输入问题。")
        continue

    messages.append({
        "role": "user",
        "content": question
    })

    # 最多允许连续处理5轮工具调用，防止无限循环
    for step in range(5):

        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=messages,
            tools=tools,
            tool_choice="auto"
        )

        message = response.choices[0].message

        # 如果模型不再请求工具，输出最终回答
        if not message.tool_calls:
            print("\n助手：", message.content)
            messages.append({
                "role": "assistant",
                "content": message.content or ""
            })
            break

        # 将模型的工具调用请求加入对话历史
        messages.append(
            message.model_dump(exclude_none=True)
        )

        # 执行模型请求的工具
        for tool_call in message.tool_calls:

            function_name = tool_call.function.name

            arguments = json.loads(
                tool_call.function.arguments
            )

            function = available_tools.get(function_name)

            if function is None:
                result = f"错误：不存在工具 {function_name}"
            else:
                try:
                    result = function(**arguments)
                except (TypeError, ValueError, KeyError) as e:
                    result = f"工具执行失败：{e}"

            print(
                f"\n[工具执行] {function_name}：{result}"
            )

            # 把工具结果交还给模型
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": str(result)
            })

    else:
        print("\n助手：工具调用次数达到上限，请重新提问。")
