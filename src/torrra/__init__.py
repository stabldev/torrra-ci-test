import importlib
import questionary
from questionary import Choice
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

    torrent_choices = [Choice(title=torrent.title, value=torrent) for torrent in torrents]
    selected_torrent: Torrent = questionary.select("Select:", choices=torrent_choices).ask()
    console.print(selected_torrent.link)
