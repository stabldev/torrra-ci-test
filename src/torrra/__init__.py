import importlib
import questionary
from typing import List
from rich.console import Console

from torrra.types import TorrentPreview

console = Console()

INDEXERS_MAP = {
    "yts.mx": "torrra.indexers.yts_mx"
}

def main() -> None:
    query = questionary.text("Search:").ask()

    if not query:
        console.print("[red]No query entered. Exiting...[/red]")
        return

    indexer_name = questionary.select("Choose an indexer:", choices=list(INDEXERS_MAP.keys())).ask()
    indexer_module_path = INDEXERS_MAP[indexer_name]

    with console.status(f"[bold green]Searching {indexer_name} for '{query}'...[/bold green]"):
        indexer = importlib.import_module(indexer_module_path)
        torrents: List[TorrentPreview] = indexer.fetch_torrents(query)

    questionary.select("Select:", choices=[torrent.title for torrent in torrents]).ask()
