import os

from dotenv import load_dotenv
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END
from langgraph.cache.memory import InMemoryCache
from langgraph.types import CachePolicy
from langsmith import Client

from src.get_hot_movie_list import GetHotMovieList
from src.select_movie import SelectMovie
from src.movie_analyzer_node import MovieAnalyzerNode
from src.lyric_producer import LyricProducer
from src.approve_lyrics import ApproveLyrics
from src.state import UserGraphState, MovieListState, OutputState


class UserGraph:

    def build_user_graph(self):
        load_dotenv(override=True)
        Client(api_key=os.getenv("LANGSMITH_API_KEY"))
        checkpointer = MemorySaver()
        ## todo 改成缓存才可以解决稳定输出，以及节省token成本
        cache = InMemoryCache()
        cache_policy = CachePolicy(ttl=10)

        builder = StateGraph(UserGraphState,input_schema=MovieListState,output_schema=OutputState)
        # get_hot_movie_list 只抓取榜单；select_movie 单独做 interrupt，两者都不配 cache_policy
        builder.add_node("get_hot_movie_list", GetHotMovieList())
        builder.add_node("select_movie", SelectMovie())
        builder.add_node("movie_analyzer", MovieAnalyzerNode(), cache_policy=cache_policy)
        builder.add_node("lyric_producer", LyricProducer())
        builder.add_node("approve_lyrics", ApproveLyrics())
        builder.set_entry_point("get_hot_movie_list")
        builder.add_edge("get_hot_movie_list", "select_movie")
        builder.add_edge("select_movie", "movie_analyzer")
        builder.add_edge("movie_analyzer", "lyric_producer")
        builder.add_edge("lyric_producer", "approve_lyrics")
        return builder.compile(checkpointer=checkpointer, cache=cache)


user_graph = UserGraph().build_user_graph()
