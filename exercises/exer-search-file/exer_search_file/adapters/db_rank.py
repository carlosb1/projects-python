"""DB adapter that  saves in memory files and their content.

It is not safe-thread but it has a semi-constant time complexity that it depends of the collisions
"""
from typing import List


class DBRanking:
    """DB adapter class.

    It represents a DB repository to save where files include one word.
    """

    def __init__(self):
        self._table = {}

    def query_by_word(self, word: str) -> List[str]:
        """Query function sarching by word.

        Args:
            word(str): Word to be searched

        Returns:
            List[str]: List of files that it includes this word

        """
        if word not in self._table:
            return []
        return self._table[word]

    def save(self, filename: str, words: List[str]):
        """Save function. It saves a set of words from a file.

        Arguments:
            filename(str): file which contains a set of words.
            words(List): it contains the content of words from the file.

        """
        for entry in words:
            if entry not in self._table:
                self._table[entry] = []
            self._table[entry].append(filename)
