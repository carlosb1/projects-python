from io import StringIO
from unittest.mock import MagicMock, Mock
from bunch import Bunch
from models import Color, Game
from adapters import RandomGeneratorAdapter
from entrypoints import CLI
from usecases import StartGame, ResponseGame
from controller import CodeMaker

RESULT_TEST = "\n->: \nINPUT    WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\n->: \nINPUT      WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\nR                   0             0\n"


def test_should_play_game_first_movement():
    # define models
    game = Game(is_started=False)
    # define entrypoints
    inp = Bunch()
    inp.readline = Mock()
    inp.readline.side_effect = ['start', 'R']
    outp = StringIO()
    outp.write("\n")
    cli = CLI(inp, outp, 1)
    # define adapters
    generator = RandomGeneratorAdapter([Color.RED], 1)
    generator.generate = MagicMock(return_value=[Color.BLUE])
    start_game = StartGame(game, generator)
    response_game = ResponseGame(game)
    # create game and run turns
    codemaker = CodeMaker(game, cli, start_game, response_game)
    codemaker.run()
    codemaker.run()
    # check final result
    assert(outp.getvalue() == RESULT_TEST)
    outp.close()


RESULT_TEST2 = "\n->: \nINPUT    WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\n->: \nINPUT      WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\nRRBB                2             0\n"


def test_should_get_white_pegs():
    # define models
    game = Game(is_started=False)
    # define entrypoints
    inp = Bunch()
    inp.readline = Mock()
    inp.readline.side_effect = ['start', 'RRBB']
    outp = StringIO()
    outp.write("\n")
    cli = CLI(inp, outp, 4)
    # define adapters
    AVAILABLE_VALUES = [color for color in Color]
    generator = RandomGeneratorAdapter(AVAILABLE_VALUES, 4)
    generator.generate = MagicMock(return_value=[Color.BLUE, Color.BLUE, Color.GREEN, Color.ORANGE])
    start_game = StartGame(game, generator)
    response_game = ResponseGame(game)
    # create game and run turns
    codemaker = CodeMaker(game, cli, start_game, response_game)
    codemaker.run()
    codemaker.run()
    # check final result
    assert(outp.getvalue() == RESULT_TEST2)
    outp.close()


RESULT_TEST3 = "\n->: \nINPUT    WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\n->: \nINPUT      WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\nBBGO                0             4\n"


def test_should_get_black_pegs():
    # define models
    game = Game(is_started=False)
    # define entrypoints
    inp = Bunch()
    inp.readline = Mock()
    inp.readline.side_effect = ['start', 'BBGO']
    outp = StringIO()
    outp.write("\n")
    cli = CLI(inp, outp, 4)
    # define adapters
    AVAILABLE_VALUES = [color for color in Color]
    generator = RandomGeneratorAdapter(AVAILABLE_VALUES, 4)
    generator.generate = MagicMock(return_value=[Color.BLUE, Color.BLUE, Color.GREEN, Color.ORANGE])
    start_game = StartGame(game, generator)
    response_game = ResponseGame(game)
    # create game and run turns
    codemaker = CodeMaker(game, cli, start_game, response_game)
    codemaker.run()
    codemaker.run()
    # check final result
    assert(outp.getvalue() == RESULT_TEST3)
    outp.close()


RESULT_TEST4 = "\n->: \nINPUT    WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\n->: \nINPUT      WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\nBGBO                2             2\n"


def test_should_get_black_and_white_pegs():
    # define models
    game = Game(is_started=False)
    # define entrypoints
    inp = Bunch()
    inp.readline = Mock()
    inp.readline.side_effect = ['start', 'BGBO']
    outp = StringIO()
    outp.write("\n")
    cli = CLI(inp, outp, 4)
    # define adapters
    AVAILABLE_VALUES = [color for color in Color]
    generator = RandomGeneratorAdapter(AVAILABLE_VALUES, 4)
    generator.generate = MagicMock(return_value=[Color.BLUE, Color.BLUE, Color.GREEN, Color.ORANGE])
    start_game = StartGame(game, generator)
    response_game = ResponseGame(game)
    # create game and run turns
    codemaker = CodeMaker(game, cli, start_game, response_game)
    codemaker.run()
    codemaker.run()
    # check final result
    assert(outp.getvalue() == RESULT_TEST4)
    outp.close()


RESULT_TEST5 = "\n->: \nThe size must be 1\n"


def test_should_throws_message_not_start():
    # define models
    game = Game(is_started=False)
    # define entrypoints
    inp = Bunch()
    inp.readline = Mock()
    inp.readline.side_effect = ['rrr']
    outp = StringIO()
    outp.write("\n")
    cli = CLI(inp, outp, 1)
    # define adapters
    generator = RandomGeneratorAdapter([Color.RED], 1)
    generator.generate = MagicMock(return_value=[Color.BLUE])
    start_game = StartGame(game, generator)
    response_game = ResponseGame(game)
    # create game and run turns
    codemaker = CodeMaker(game, cli, start_game, response_game)
    codemaker.run()
    assert(outp.getvalue() == RESULT_TEST5)
