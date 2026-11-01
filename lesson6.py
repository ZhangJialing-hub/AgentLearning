import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 读取 API Key
load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 API Key")

# 2. 创建客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 3. 保存对话历史
messages = [
    {
        "role": "system",
        "content": "你是一个友好的大学生学习助手。"
    }
]

# 4. 定义多轮对话函数
def ask_model(question):
    # 把用户的问题加入历史记录
    messages.append({
        "role": "user",
        "content": question
    })

    # 把完整对话历史发送给模型
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=messages
    )

    # 获取 AI 的回答
    answer = response.choices[0].message.content

    # 把 AI 的回答也加入历史记录
    messages.append({
        "role": "assistant",
        "content": answer
    })

    return answer


# 5. 循环接收用户输入
print("学习助手已启动！输入 exit 退出。")

while True:
    question = input("你：")

    if question.lower() == "exit":
        print("学习助手已退出。")
        break

    if not question.strip():
        print("请输入有效的问题。")
        continue

    result = ask_model(question)
    print("AI：", result)
