import os
from dotenv import load_dotenv
from openai import OpenAI

# 读取环境变量
load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")

if not api_key:
    raise ValueError("没有找到 API Key")

# 创建客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 定义一个调用 AI 的函数
def ask_model(question):
    response = client.chat.completions.create(
        model="deepseek-flash",
        messages=[
            {
                "role": "system",
                "content": "你是一个友好的大学生学习助手。"
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    answer = response.choices[0].message.content

    return answer


# 调用函数
result = ask_model("请给我制定一个今天的算法学习计划")

print("AI 的回答：")
print(result)