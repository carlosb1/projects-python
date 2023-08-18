"""Classes to represent our domain problem. It means our reqs and domain classes.

In this case, our domain classes are minimal, they could be `Path` classes and for future
implementation we could move `Dict` classes to some dataclass for representing better
our domain. It was not done to avoid overcomplicate the problem.

"""

from typing import List, Tuple, Dict
from exer_search_file.adapters.db_rank import DBRanking
from exer_search_file.adapters.file_loader import FileLoader
from pathlib import Path

TOP_VALUES = 10


class Searcher:
    """Use case to implement searches.

    It searchs inside our db `db_ranking` for files and sort the top x values with
    `top_values`.

    Args:
        db_ranking(DBRanking): DB repository to save word s file.
        top_values(int): Top de values to return.

    """

    def __init__(self, db_ranking: DBRanking, top_values=TOP_VALUES):
        self._db_ranking = db_ranking
        self._top_values = top_values

    def run(self, words: List[str]) -> List[Tuple[str, float]]:
        """Run use case and search words `words`.

        Args:
            words (List): List of words to search.

        Returns:
            List with file and their found word s percentage.

        """
        files_found_by_word = self._count_words_in_file(words)
        found_files_with_percentage = self._calculate_ranking(files_found_by_word, words)
        sorted_results = self._calculate_top(found_files_with_percentage)
        return sorted_results

    def _count_words_in_file(self, words: List[str]) -> Dict[str, int]:
        """Count found words for saved file in db."""
        files_found_by_word = {}
        for word in words:
            found_files_with_word = self._db_ranking.query_by_word(word)
            for filename in found_files_with_word:
                if filename not in files_found_by_word:
                    files_found_by_word[filename] = 0
                files_found_by_word[filename] = files_found_by_word[filename] + 1

        return files_found_by_word

    def _calculate_ranking(self, files_found_by_word: Dict[str, int],
                           words: List[str]) -> List[Tuple[str, float]]:
        """It calculates percentage of found words."""
        size_words = len(words)
        words_percentage_hit = [(k, v / size_words) for (k, v) in files_found_by_word.items()]
        return words_percentage_hit

    def _calculate_top(self,
                       words_percentage_hit: List[Tuple[str, float]]) -> List[Tuple[str, float]]:
        """It calculates top of values."""
        return sorted(words_percentage_hit, key=(lambda tup: tup[1]))[:self._top_values]


class Loader:
    """Use case to load initial information from one path file.

    Args:
        db_ranking(DBRanking): DB repository to save word s file.
        file_loader(FileLoader): Adapter to load filesytem files and content.

    """

    def __init__(self, db_ranking: DBRanking, file_loader: FileLoader):
        self._db_ranking = db_ranking
        self._file_loader = file_loader

    def run(self, path_db: Path):
        """Run  use case loading info from path.

        Args:
            path_db(Path): Directory path to be loaded.

        """
        found_files = self._file_loader.load(path_db)
        for key, value in found_files.items():
            self._db_ranking.save(key, value)
