"""CLI user interface as entrypoint.

This entrypoint is a specific type of adapter that it works as entrypoint for our code.i
"""

from pathlib import Path
from typing import List, Tuple

from exer_search_file.domain import Searcher, Loader


class CLI:
    """CLI user interface. It loads uses cases that they must be executed.

    Args:
        seacher(Searcher): Search use case.
        loader(Loader): Loader use case.

    """

    def __init__(self, _searcher: Searcher, _loader: Loader):
        self._searcher = _searcher
        self._loader = _loader

    def start(self, path_db: str):
        """Start function to start cli.

        It loads directory information and run the repl command line.

        Args:
            path_db (str): Path directory to search files and words.


        """
        path = Path(path_db)
        self._loader.run(path)
        self._run_repl()

    def _run_repl(self):
        text = input('>>>: ')
        if text:
            found_results = self._searcher.run(text.replace('\n', '').split())
            self._print_results(found_results)

    def _print_results(self, results: List[Tuple[str, float]]):
        for (fil, percen) in results:
            normalized_percen = int(percen * 100.0)
            print(f'{fil}: {normalized_percen}%')
