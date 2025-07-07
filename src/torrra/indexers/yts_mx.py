from selectolax.parser import HTMLParser
from torrra.helpers.html import parse_html

def fetch_torrents(query: str) -> list[str]:
    url = f"https://yts.mx/browse-movies/{query}/all/all/0/latest/0/all"
    res = []

    html = parse_html(url)
    parser = HTMLParser(html)

    nodes = parser.css(".browse-content .browse-movie-wrap .browse-movie-bottom")
    for node in nodes:
        title_node = node.css_first(".browse-movie-title")
        year_node = node.css_first(".browse-movie-year")

        title = title_node.text() if title_node else ""
        year = year_node.text() if year_node else ""

        res.append(title + " " + year)

    return res
