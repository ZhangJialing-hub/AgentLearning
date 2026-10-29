import os
from dotenv import load_dotenv
from openai import OpenAI

# 1. 读取 .env 文件中的环境变量
load_dotenv()

# 2. 获取 API Key
api_key = os.getenv("DEEPSEEK_API_KEY")

# 3. 检查密钥是否存在
if not api_key:
    raise ValueError("没有找到 DEEPSEEK_API_KEY，请检查 .env 文件")

# 4. 创建客户端，指定 DeepSeek 的 API 地址
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com"
)

# 5. 发送问题给大模型
response = client.chat.completions.create(
    model="deepseek-flash",
    messages=[
        {
            "role": "system",
            "content": "你是一名善于帮助大学生安排学习计划的助手。"
        },
        {
            "role": "user",
            "content": "我今天有2小时，请帮我安排一个简单的Python学习计划。"
        }
    ]
)

# 6. 打印模型返回的回答
answer = response.choices[0].message.content
print("DeepSeek 的回答：")
print(answer)