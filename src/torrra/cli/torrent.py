from typing import List

import questionary
from prompt_toolkit.shortcuts import CompleteStyle
from questionary import Choice

from torrra.constants import UI_STRINGS
from torrra.context import console
from torrra.core.config import Config
from torrra.core.downloader import download_magnet
from torrra.indexers import INDEXERS_MAP
from torrra.types import Torrent
from torrra.utils import styles, welcome

config = Config()


def run_torrent_flow() -> None:
    welcome.show_welcome()

    query = questionary.text(UI_STRINGS["prompt_search_query"], style=styles.TEXT).ask()
    if not query:
        return

    indexer_name = questionary.select(
        UI_STRINGS["prompt_choose_indexer"],
        choices=list(INDEXERS_MAP.keys()),
        style=styles.SELECT,
    ).ask()
    if not indexer_name:
        return

    with console.status(
        UI_STRINGS["status_searching"].format(indexer=indexer_name, query=query)
    ):
        max_results = config.get("general.max_results") or None
        torrents: List[Torrent] = INDEXERS_MAP[indexer_name]().search(
            query, max_results
        )

    if not torrents:
        console.print(UI_STRINGS["error_no_results"])
        return

    torrent_choices = [
        Choice(title=torrent.title, value=torrent) for torrent in torrents
    ]

    selected_torrent: Torrent | None = questionary.select(
        UI_STRINGS["prompt_select_result"],
        choices=torrent_choices,
        style=styles.SELECT,
    ).ask()
    if not selected_torrent:
        return

    default_path = config.get("general.download_path")
    save_path = questionary.path(
        UI_STRINGS["prompt_download_path"],
        default=default_path,
        only_directories=True,
        complete_style=CompleteStyle.COLUMN,
        style=styles.TEXT,
    ).ask()
    if not save_path:
        return

    if save_path != default_path and config.get("general.remember_last_path"):
        config.set("general.download_path", save_path)

    # initiate download
    download_magnet(selected_torrent.magnet_uri, save_path)
