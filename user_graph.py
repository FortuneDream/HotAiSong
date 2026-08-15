import os
from typing import TypedDict

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langsmith import Client

from movie_analyzer_node import MovieAnalyzerNode
from lyric_producer import LyricProducer


class UserGraphState(TypedDict):
    prompt: str
    full_text: str
    lyrics: str


def build_user_graph():
    load_dotenv(override=True)
    Client(api_key=os.getenv("LANGSMITH_API_KEY"))
    checkpointer = MemorySaver()
    builder = StateGraph(UserGraphState)
    builder.add_node("movie_analyzer", MovieAnalyzerNode())
    builder.add_node("lyric_producer", LyricProducer())
    builder.set_entry_point("movie_analyzer")
    builder.add_edge("movie_analyzer", "lyric_producer")
    builder.add_edge("lyric_producer", END)

    return builder.compile(checkpointer=checkpointer)


user_graph = build_user_graph()
