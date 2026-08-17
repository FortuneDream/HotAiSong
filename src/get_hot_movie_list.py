import re
from typing import List

import requests
from bs4 import BeautifulSoup

from src.state import MovieListState


class GetHotMovieList:
    """抓取猫眼电影榜单，打印列表并存入 state.movie_list，供下一个节点选择。"""

    MAOYAN_URL = "https://www.maoyan.com/board/"
    HEADERS = {
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,image/apng,*/*;q=0.8,"
            "application/signed-exchange;v=b3;q=0.7"
        ),
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://www.maoyan.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/131.0.0.0 Safari/537.36"
        ),
    }

    def _fetch_movie_list(self) -> List[str]:
        session = requests.Session()
        session.headers.update(self.HEADERS)
        # 先访问主页，建立 Cookie
        try:
            session.get("https://www.maoyan.com/", timeout=15)
        except requests.RequestException:
            pass
        resp = session.get(self.MAOYAN_URL, timeout=15)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        movie_names: List[str] = []
        items = soup.select("dd")
        for item in items:
            name_tag = item.select_one("p.name a, .movie-item-info .name a")
            if name_tag:
                name = name_tag.get_text(strip=True)
                if name:
                    movie_names.append(name)

        if not movie_names:
            text_pattern = re.findall(
                r"^\s*\d+\s*[\r\n]+(.+?)(?:\r?\n|主演)", soup.get_text(), re.MULTILINE
            )
            for name in text_pattern:
                name = name.strip()
                if name and name not in movie_names:
                    movie_names.append(name)

        return movie_names

    def __call__(self, state: MovieListState) -> dict:
        print("get hot movie list node")
        movie_list = self._fetch_movie_list()

        if not movie_list:
            raise RuntimeError("未能抓取到电影榜单，请检查网络或稍后重试。")

        print("\n=== 猫眼热映电影榜单 TOP %d ===" % len(movie_list))
        for idx, name in enumerate(movie_list, start=1):
            print(f"  {idx}. {name}")
        print()

        return {"movie_list": movie_list}
