from langgraph.types import Command

from src.user_graph import user_graph


if __name__ == "__main__":
    config = {"configurable": {"thread_id": "1"}}
    result = user_graph.invoke({"prompt": "唐伯虎点秋香"}, config=config)

    while "__interrupt__" in result:
        # 阻塞程序，等待用户输入
        answer = input("你对生成的歌词满意吗？(y/n): ").strip()
        # 这里的answer是在下一次调用interupt的时候，会直接传入resume值（也就是恢复的时候）
        result = user_graph.invoke(Command(resume=answer), config=config)

    print("\n=== 结束流程 ===")

