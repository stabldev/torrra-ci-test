import importlib
import questionary
from typing import List
from rich.console import Console

from torrra.indexers import INDEXERS
from torrra.types import Torrent

console = Console()

def main() -> None:
    query = questionary.text("Search:").ask()

    if not query:
        console.print("[red]No query entered. Exiting...[/red]")
        return

    indexer_name = questionary.select("Choose an indexer:", choices=list(INDEXERS.keys())).ask()
    indexer_module_path = INDEXERS[indexer_name]
    indexer = importlib.import_module(indexer_module_path).Indexer()

    with console.status(f"[bold green]Searching {indexer_name} for '{query}'...[/bold green]"):
        torrents: List[Torrent] = indexer.search(query)

    if not torrents:
        console.print("[red]Cound not find any torrent. Exiting...[/red]")
        return

    questionary.select("Select:", choices=[torrent.title for torrent in torrents]).ask()
