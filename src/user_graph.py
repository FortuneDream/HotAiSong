import os

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy
from langsmith import Client

from src.movie_analyzer_node import MovieAnalyzerNode
from src.lyric_producer import LyricProducer
from src.state import UserGraphState, InputState, OutputState


class UserGraph:

    def build_user_graph(self):
        load_dotenv(override=True)
        Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        checkpointer = MemorySaver()
        ## todo 改成缓存才可以解决稳定输出，以及节省token成本
        cache = InMemoryCache()
        cache_policy = CachePolicy(ttl=10)

        builder = StateGraph(UserGraphState,input_schema=InputState,output_schema=OutputState)
        builder.add_node("movie_analyzer", MovieAnalyzerNode(), cache_policy=cache_policy)
        builder.add_node("lyric_producer", LyricProducer(), cache_policy=cache_policy)
        builder.set_entry_point("movie_analyzer")
        builder.add_edge("movie_analyzer", "lyric_producer")
        builder.add_edge("lyric_producer", END)

        return builder.compile(checkpointer=checkpointer, cache=cache)


user_graph = UserGraph().build_user_graph()
