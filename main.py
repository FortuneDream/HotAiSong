from src.user_graph import user_graph


if __name__ == "__main__":
    user_graph.invoke(
        {"prompt": "唐伯虎点秋香"},
        config={"configurable": {"thread_id": "1"}},
    )
    print("\n-----------------第一次\n")
    user_graph.invoke(
        {"prompt": "唐伯虎点秋香"},
        config={"configurable": {"thread_id": "1"}},
    )
    print("\n-----------------第二次\n")
