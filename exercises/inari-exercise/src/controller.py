from entrypoints import UserEntrypoint
from usecases import StartGame, ResponseGame
from models import Status


class CodeMaker():
    """
        Controller module to call diferent use cases and join with inverse dependencies all the clean architecure
        modules
    """
    def __init__(self, game, input_entrypoint: UserEntrypoint, start_game: StartGame, response_game: ResponseGame):
        self._game = game
        self._input_entrypoint = input_entrypoint
        self._start_game = start_game
        self._response_game = response_game

    def run(self):
        self._input_entrypoint.ask()
        result = self._input_entrypoint.get_code()
        finish = False
        if result.get_start():
            self._start_game.run()
        elif (self._game.is_started and result.get_input_value() != []):
                finish = self._response_game.run(result.get_input_value())
                finish = (finish != Status.PLAY)
        if self._game.is_started:
            self._input_entrypoint.response(self._game.results)
        return finish

    @staticmethod
    def makeCodeMaker(size_to_search, num_tries):
        import sys
        from models import Color, Game
        from entrypoints import CLI
        from adapters import RandomGeneratorAdapter

        AVAILABLE_VALUES = [color for color in Color]
        game = Game(is_started=False)
        # define entrypoints
        cli = CLI(sys.stdin, sys.stdout, size_to_search)
        # define adapters
        generator = RandomGeneratorAdapter(AVAILABLE_VALUES, size_to_search)
        # define use cases
        start_game = StartGame(game, generator)
        response_game = ResponseGame(game, num_tries)
        codemaker = CodeMaker(game, cli, start_game, response_game)
        return codemaker
