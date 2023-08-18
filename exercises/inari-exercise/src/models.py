from enum import Enum


class Color(Enum):
    RED = 'R'
    BLUE = 'B'
    YELLOW = 'Y'
    GREEN = 'G'
    WHITE = 'W'
    ORANGE = 'O'


class Status(Enum):
    PLAY = 0
    WIN = 1
    LOST = 2


class Game(object):
    """
        Business domain to represent a game.
    """
    def __init__(self, value_to_find=None, results=[], is_started=None, tries=None):
        self._value_to_find = value_to_find
        self._results = results
        self._is_started = is_started
        self._tries = tries

    @property
    def value_to_find(self):
        return self._value_to_find

    @property
    def results(self):
        return self._results

    @property
    def is_started(self):
        return self._is_started

    @property
    def tries(self):
        return self._tries

    @value_to_find.setter
    def value_to_find(self, value):
        self._value_to_find = value

    @results.setter
    def results(self, value):
        self._results = value

    @is_started.setter
    def is_started(self, value):
        self._is_started = value

    @tries.setter
    def tries(self, value):
        self._tries = value

    @value_to_find.deleter
    def value_to_find(self):
        return self._value_to_find

    @results.deleter
    def results(self):
        return self._results

    @is_started.deleter
    def is_started(self):
        return self._is_started

    @tries.deleter
    def tries(self):
        return self._tries
