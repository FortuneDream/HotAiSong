from typing import TypedDict, List


class UserGraphState(TypedDict):
    movie_list: List[str]
    movie_name: str
    movie_brief_text: str
    lyrics: str
    approved: bool

class MovieState(TypedDict):
     movie_name: str

class OutputState(TypedDict):
    lyrics: str

class MovieListState(TypedDict):
    movie_list: List[str]

class MovieAnalyzerState(TypedDict):
    movie_brief_text: str

class LyricProducerState(TypedDict):
    lyrics: str