from typing import List

from torrra.indexers.base import BaseIndexer
from torrra.types import TorrentPreview

class Indexer(BaseIndexer):
    def search(self, query: str) -> List[TorrentPreview]:
        url = f"https://yts.mx/browse-movies/{query}/all/all/0/latest/0/all"
        parser = self._get_parser(url)
        res = []

        nodes = parser.css("div.browse-content div.browse-movie-wrap div.browse-movie-bottom")
        for node in nodes:
            title_node = node.css_first("a.browse-movie-title")
            year_node = node.css_first("div.browse-movie-year")

            title = title_node.text(strip=True) if title_node else ""
            link = title_node.attributes.get("href") if title_node else ""

            if query not in title.lower() or link is None:
                continue

            year = year_node.text(strip=True) if year_node else ""

            torrent_title = f"{title} {year}".strip()
            res.append(TorrentPreview(title=torrent_title, link=link))

        return res
