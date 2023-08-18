import pytest
from unittest.mock import MagicMock
from bunch import Bunch
from models import Color, Status, Game
from adapters import RandomGeneratorAdapter
from usecases import StartGame, ResponseGame


def test_should_give_start_correctly():
    game = Game()
    generator = RandomGeneratorAdapter([Color.RED], 1)
    generator.generate = MagicMock(return_value=[Color.BLUE])
    start = StartGame(game, generator)
    start.run()
    assert(game.value_to_find == [Color.BLUE])


def test_should_have_same_size():
    game = Game(value_to_find=[Color.RED], results=[], tries=0)
    response = ResponseGame(game)
    with pytest.raises(ValueError):
        assert(response.run([Color.BLUE, Color.RED]))


def assert_response(result, game, is_resolved, check_first_value):
    assert(result == is_resolved)
    assert(len(game.results) == 1)
    assert(game.results[0] == check_first_value)


def test_should_response_fail_value_correctly():
    game = Game(value_to_find=[Color.RED], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.BLUE])
    assert_response(result, game, Status.PLAY, Bunch(input=[Color.BLUE], number_white_pegs=0, number_black_pegs=0))


def test_should_response_has_not_white_pegs():
    game = Game(value_to_find=[Color.RED, Color.WHITE, Color.RED, Color.WHITE], results=[], tries=0)
    response = ResponseGame(game)
    response.run([Color.WHITE, Color.WHITE, Color.WHITE, Color.WHITE])
    assert(game.results[0].number_black_pegs == 2)
    assert(game.results[0].number_white_pegs == 0)


def test_should_stop_after_num_tries():
    game = Game(value_to_find=[Color.RED], results=[], tries=0)
    response = ResponseGame(game, num_tries=1)
    result = response.run([Color.BLUE])
    assert(result == Status.LOST)


def test_should_response_wins_correctly():
    game = Game(value_to_find=[Color.BLUE], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.BLUE])
    assert_response(result, game, Status.WIN, Bunch(input=[Color.BLUE], number_white_pegs=0, number_black_pegs=1))


def test_should_response_white_peg_correctly():
    game = Game(value_to_find=[Color.RED, Color.GREEN], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.GREEN, Color.BLUE])
    assert_response(result, game, Status.PLAY, Bunch(input=[Color.GREEN, Color.BLUE], number_white_pegs=1, number_black_pegs=0))


def test_should_response_multiple_white_pegs_correctly():
    game = Game(value_to_find=[Color.RED, Color.GREEN], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.GREEN, Color.RED])
    assert_response(result, game, Status.PLAY, Bunch(input=[Color.GREEN, Color.RED], number_white_pegs=2, number_black_pegs=0))


def test_should_response_multiple_black_pegs_correctly():
    game = Game(value_to_find=[Color.RED, Color.GREEN], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.RED, Color.GREEN])
    assert_response(result, game, Status.WIN, Bunch(input=[Color.RED, Color.GREEN], number_white_pegs=0, number_black_pegs=2))


def test_should_response_multiple_black_and_white_pegs_correctly():
    game = Game(value_to_find=[Color.RED, Color.GREEN, Color.RED, Color.WHITE], results=[], tries=0)
    response = ResponseGame(game)
    result = response.run([Color.RED, Color.GREEN, Color.GREEN, Color.RED])
    assert_response(result, game, Status.PLAY, Bunch(input=[Color.RED, Color.GREEN, Color.GREEN, Color.RED], number_white_pegs=1, number_black_pegs=2))
