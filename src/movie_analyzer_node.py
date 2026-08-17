import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_deepseek import ChatDeepSeek
from src.state import MovieState


class MovieAnalyzerNode:
    SYSTEM_PROMPT = "你是一个电影人，你的主要回答当用户提问关键词是电影名字时，你告诉他这个电影主要讲的是什么事情，语言要简练"

    def __init__(self):
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            temperature=0,
            seed=1,
            top_p=1.0,
        )

    def __call__(self, state: MovieState):
        print("movie analyzer node")
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=state["movie_name"]),
        ]
        full_text_chunks = []
        for chunk in self.llm.stream(messages):
            text = chunk.content
            if text:
                full_text_chunks.append(text)
                print(text, end="", flush=True)
        print("\n")
        return {"movie_brief_text": "".join(full_text_chunks)}
