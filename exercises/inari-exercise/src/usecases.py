from adapters import GeneratorAdapter
from bunch import Bunch
from models import Status


class StartGame():
    """
        use case to initialize new game
    """
    def __init__(self, game, generator: GeneratorAdapter):
        self._generator = generator
        self._game = game

    def run(self):
        self._game.value_to_find = self._generator.generate()
        self._game.results = []
        self._game.is_started = True
        self._game.tries = 0


class ResponseGame():
    """
        use case to play a game and response.
    """
    def __init__(self, game, num_tries=10):
        self._game = game
        self._num_tries = num_tries

    def run(self, input_value):
        if (len(self._game.value_to_find) != len(input_value)):
            raise ValueError("It must have the same size")
        number_black_pegs = 0
        number_white_pegs = 0
        input_value_repeated = input_value.copy()
        values_to_search_repeated = self._game.value_to_find.copy()
        # search black pegs
        for index, in_color in enumerate(input_value):
            if (self._game.value_to_find[index] == in_color):
                number_black_pegs += 1
                values_to_search_repeated.remove(in_color)
                input_value_repeated.remove(in_color)
        # search white pegs with discarded
        for in_color in input_value_repeated:
            if (in_color in values_to_search_repeated):
                number_white_pegs += 1

        self._game.results.append(Bunch(input=input_value, number_white_pegs=number_white_pegs, number_black_pegs=number_black_pegs))
        result = Status.PLAY
        if number_black_pegs == len(self._game.value_to_find):
            result = Status.WIN
        else:
            self._game.tries += 1
            if self._game.tries >= self._num_tries:
                result = Status.LOST
        return result
