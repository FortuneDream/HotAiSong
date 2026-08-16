import os

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langsmith import Client

from src.movie_analyzer_node import MovieAnalyzerNode
from src.lyric_producer import LyricProducer
from src.state import UserGraphState


class UserGraph:

    def build_user_graph(self):
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


user_graph = UserGraph().build_user_graph()
