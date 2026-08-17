import os

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_deepseek import ChatDeepSeek
from src.state import MovieAnalyzerState



class LyricProducer:
    SYSTEM_PROMPT = "你是一个词作者，根据给定的电影简介，创作一段与电影主题相关的歌词，语言优美、情感真挚。只需要创作一段主歌，一段副歌即可"

    def __init__(self):
        self.llm = ChatDeepSeek(
            model="deepseek-chat",
            api_key=os.getenv("DEEPSEEK_API_KEY"),
            temperature=0,
        )

    def __call__(self, state: MovieAnalyzerState):
        print("lyric producer node")
        messages = [
            SystemMessage(content=self.SYSTEM_PROMPT),
            HumanMessage(content=f"电影简介：{state['movie_brief_text']}"),
        ]
        lyrics_chunks = []
        for chunk in self.llm.stream(messages):
            text = chunk.content
            if text:
                lyrics_chunks.append(text)
                print(text, end="", flush=True)
        print("\n")
        return {"lyrics": "".join(lyrics_chunks)}
