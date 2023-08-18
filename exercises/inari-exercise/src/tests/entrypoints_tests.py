from unittest.mock import MagicMock
from io import StringIO
from bunch import Bunch
from entrypoints import CLI, QUESTION
from models import Color


RESULT_TEST = "INPUT      WHITE_PEGS    BLACK_PEGS\n-------  ------------  ------------\nRRBB                0             0\n"


def test_should_inserts_code_correctly():
    inp = Bunch()
    inp.readline = MagicMock(return_value='RRBB')
    outp = StringIO()

    cli = CLI(inp, outp)
    cli.ask()
    code = cli.get_code()
    assert(outp.getvalue() == (QUESTION + '\n') and code.get_input_value() == [Color.RED, Color.RED, Color.BLUE, Color.BLUE])


def test_should_starts_correctly():
    outp = StringIO()
    inp = Bunch()
    inp.readline = MagicMock(return_value='start')
    cli = CLI(inp, outp)
    assert(cli.get_code().get_start())


def test_should_print_response_correctly():
    outp = StringIO()
    cli = CLI(["RRBB"], outp)
    results = [Bunch(input=[Color.RED, Color.RED, Color.BLUE, Color.BLUE], number_white_pegs=0, number_black_pegs=0)]
    cli.response(results)
    assert(outp.getvalue() == RESULT_TEST)


def test_should_print_error_not_correct_size():
    outp = StringIO()
    inp = Bunch()
    inp.readline = MagicMock(return_value='')
    cli = CLI(inp, outp)
    code = cli.get_code()
    assert(code.get_input_value() == [] and outp.getvalue() == "The size must be 4\n")


def test_should_print_error_not_correct_color():
    inp = Bunch()
    inp.readline = MagicMock(return_value='RSBB')
    outp = StringIO()
    cli = CLI(inp, outp)
    code = cli.get_code()
    assert(code.get_input_value() == [] and outp.getvalue() == "The color must be one of RBYGWO (Red Blue Yellow Green White Orange)\n")
