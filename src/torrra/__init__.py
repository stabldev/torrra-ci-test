import importlib
import questionary
from questionary import Choice
from typing import List
from rich.console import Console

from torrra.indexers import INDEXERS
from torrra.types import Magnet, Torrent

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
        console.print("[yellow]Could not find any torrents. Exiting...[/yellow]")
        return

    torrent_choices = [Choice(title=torrent.title, value=torrent) for torrent in torrents]
    selected_torrent: Torrent | None = questionary.select("Select a torrent:", choices=torrent_choices).ask()

    if not selected_torrent:
        console.print("[yellow]No torrent selected. Exiting...[/yellow]")
        return

    with console.status(f"[bold green]Fetching magnet links for '{selected_torrent.title}'...[/bold green]"):
        magnets: List[Magnet] = indexer.get_magnets(selected_torrent.link)

    if not magnets:
        console.print("[yellow]No magnet links found. Exiting...[/yellow]")
        return

    magnet_choices = [Choice(title=magnet.title, value=magnet) for magnet in magnets]
    selected_magnet: Magnet | None = questionary.select("Select:", choices=magnet_choices).ask()

    if not selected_magnet:
        console.print("[yellow]No magnet selected. Exiting...[/yellow]")
        return

    console.print(f"[green]Magnet link:[/green] {selected_magnet.magnet_uri}")
