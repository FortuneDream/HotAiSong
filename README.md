# HotAiSong

基于 **LangGraph** 编排的「电影歌词生成」工作流。从猫眼电影榜单抓取热映影片，由用户选片后，调用 DeepSeek 大模型生成电影简介与主题歌词，并支持人工确认与不满意重写的循环流程。

## 工作流程

```
START
  │
  ▼
get_hot_movie_list   抓取猫眼榜单 TOP10，存入 state.movie_list
  │
  ▼
select_movie         interrupt 等待用户输入编号，选中电影名写入 state.movie_name
  │
  ▼
movie_analyzer       DeepSeek 根据电影名生成简介，写入 state.movie_brief_text
  │
  ▼
lyric_producer       DeepSeek 根据简介创作歌词，写入 state.lyrics
  │
  ▼
approve_lyrics       interrupt 等待用户确认是否满意
  │
  ├─ 满意 (y) ──► END
  │
  └─ 不满意 (n) ─► 回到 lyric_producer 重新生成
```

两次 `interrupt`（选片 + 确认歌词）构成人机交互闭环，通过 `Command(goto=...)` 实现不满意时的循环重写。

## 技术栈

| 领域 | 技术 | 用途 |
|------|------|------|
| 工作流编排 | LangGraph 1.1.2 | 状态图、节点编排、检查点、缓存策略 |
| 人机交互 | langgraph `interrupt` / `Command` | 挂起等待用户输入、动态路由 |
| 检查点 | `MemorySaver` | 进程内状态持久化，支持 resume |
| 缓存 | `InMemoryCache` + `CachePolicy(ttl=10)` | 节点结果缓存，稳定输出并节省 token |
| 大模型调用 | LangChain 1.2.12 + langchain-deepseek | 统一 LLM 接口 |
| 大模型 | DeepSeek Chat | 电影简介 + 歌词生成（temperature=0, seed=1） |
| 网页抓取 | requests + BeautifulSoup4 | 抓取猫眼榜单 HTML 并解析电影名 |
| 配置管理 | python-dotenv | 读取 `.env` 中的 API Key |
| 可观测 | LangSmith | 运行追踪与调试 |
| 运行环境 | Python 3.11 | 入口 `main.py` |

## 项目结构

```
HotAiSong/
├── src/
│   ├── __init__.py
│   ├── state.py                # TypedDict 状态定义（UserGraphState 及各节点子状态）
│   ├── get_hot_movie_list.py   # 抓取猫眼榜单节点
│   ├── select_movie.py          # 用户选片 interrupt 节点
│   ├── movie_analyzer_node.py  # DeepSeek 生成电影简介节点
│   ├── lyric_producer.py       # DeepSeek 生成歌词节点
│   ├── approve_lyrics.py       # 用户确认 + Command 路由节点
│   └── user_graph.py           # LangGraph 图编排与编译
├── main.py                     # 入口：invoke + resume 循环
├── requirements_full.txt       # 完整依赖清单
└── .gitignore
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements_full.txt
```

### 2. 配置环境变量

在项目根目录创建 `.env` 文件：

```
DEEPSEEK_API_KEY=你的 DeepSeek API Key
LANGSMITH_API_KEY=你的 LangSmith API Key
```

### 3. 运行

```bash
python main.py
```

运行后流程：
1. 自动抓取猫眼热映榜单并打印 TOP10
2. 终端提示「请选择要生成歌词的电影编号 (1-10):」，输入编号
3. DeepSeek 生成电影简介并流式打印
4. DeepSeek 根据简介创作歌词并流式打印
5. 终端提示「等待用户确认是否满意生成的歌词」，输入 `y` 结束，输入 `n` 重新生成歌词
