from typing import TypedDict


class UserGraphState(TypedDict):
    prompt: str
    movie_brief_text: str
    lyrics: str
    approved: bool

class InputState(TypedDict):
    prompt: str

class OutputState(TypedDict):
    lyrics: str
class MovieAnalyzerState(TypedDict):
    movie_brief_text: str

class LyricProducerState(TypedDict):
    lyrics: str