from typing import Literal

from langgraph.graph import END
from langgraph.types import interrupt, Command

from src.state import UserGraphState


class ApproveLyrics:
    """获取用户确认并通过 Command 决定下一步走向。"""

    def __call__(self, state: UserGraphState) -> Command[Literal["lyric_producer", "__end__"]]:
        answer = interrupt("等待用户确认是否满意生成的歌词")
        approved = answer.strip().lower() in ("y", "yes", "满意", "满意了")

        goto = END if approved else "lyric_producer"
        return Command(
            goto=goto,
            update={"approved": approved},
        )
