from langgraph.types import interrupt

from src.state import MovieListState


class SelectMovie:
    """从 state.movie_list 中 interrupt 获取用户选择，将选中电影名写入 state.prompt。"""

    def __call__(self, state: MovieListState) -> dict:
        movie_list = state.get("movie_list", [])
        if not movie_list:
            raise RuntimeError("movie_list 为空，无法选择电影。")

        answer = interrupt("请选择要生成歌词的电影编号 (1-%d): " % len(movie_list))

        try:
            choice = int(answer.strip()) - 1
            if choice < 0 or choice >= len(movie_list):
                raise ValueError
        except (ValueError, TypeError):
            choice = 0

        selected = movie_list[choice]
        print(f"已选择: {selected}")

        return {"movie_name": selected}
