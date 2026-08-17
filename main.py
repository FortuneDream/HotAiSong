from langgraph.types import Command

from src.user_graph import user_graph


def main():
    config = {"configurable": {"thread_id": "1"}}

    # 第一步：进入 get_hot_movie_list 节点，抓取榜单并等待用户选择电影
    result = user_graph.invoke({}, config=config)

    while "__interrupt__" in result:
        # interrupt 节点会将自定义提示文字放在 result["__interrupt__"][0].value
        try:
            prompt_text = result["__interrupt__"][0].value
        except (KeyError, IndexError, AttributeError):
            prompt_text = "请输入: "
        # 阻塞程序，等待用户输入（选电影编号 或 歌词满意 y/n）
        answer = input(str(prompt_text)).strip()
        result = user_graph.invoke(Command(resume=answer), config=config)


if __name__ == "__main__":
    main()
