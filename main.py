import os

from dotenv import load_dotenv
from langchain_deepseek import ChatDeepSeek
from langsmith import Client


def query_llm(prompt: str):
    load_dotenv(override=True)
    Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    llm = ChatDeepSeek(
        model="deepseek-chat",
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        temperature=0.3,
    )

    for chunk in llm.stream(prompt):
        yield chunk.content


if __name__ == "__main__":
    user_prompt = input("请输入提示词：").strip()
    if not user_prompt:
        print("提示词不能为空")
        exit(1)

    try:
        for chunk in query_llm(user_prompt):
            print(chunk, end="", flush=True)
    except Exception as e:
        print(f"\n查询失败：{e}")
