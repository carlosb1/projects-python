import abc
from tabulate import tabulate
from models import Color
from typing import List

QUESTION = "->: "
ERROR_SIZE = "The size must be %d\n"
ERROR_COLOR = "The color must be one of RBYGWO (Red Blue Yellow Green White Orange)\n"
COLUMNS = ["INPUT", "WHITE_PEGS", "BLACK_PEGS"]


class DTOResult:
    """
        DTO object to send information among entrypoints and use cases
    """
    def __init__(self, start: bool, input_value: List[Color]):
        self._start = start
        self._input_value = input_value

    def get_start(self) -> bool:
        return self._start

    def get_input_value(self) -> List[Color]:
        return self._input_value


class UserEntrypoint(abc.ABC):
    """
        Contract for entrypoints
    """
    @abc.abstractmethod
    def ask(self):
        pass

    @abc.abstractmethod
    def response(self, results):
        pass

    @abc.abstractmethod
    def get_code(self) -> DTOResult:
        pass


class CLI(UserEntrypoint):
    """
        CLI entrypoint
    """
    AVAILABLE_VALUES = [color.value for color in Color]

    def __init__(self, inp, outp, size_input=4):
        self.inp = inp
        self.outp = outp
        self.size_input = size_input

    def ask(self):
        self.outp.write(QUESTION + '\n')

    def response(self, results):
        to_print = []
        for result in results:
            input_string = [v.value for v in result.input]
            val = ''.join(input_string)
            to_print.append([val, result.number_white_pegs, result.number_black_pegs])
        self.outp.write(tabulate(to_print, COLUMNS) + '\n')

    def get_code(self) -> DTOResult:
        line = self.inp.readline().rstrip()
        if (line.upper().rstrip() == "START"):
            return DTOResult(True, [])

        if len(line) != self.size_input:
            self.outp.write(ERROR_SIZE % (self.size_input))
            return DTOResult(False, [])

        result = []
        for value in line:
            if value not in CLI.AVAILABLE_VALUES:
                self.outp.write(ERROR_COLOR)
                return DTOResult(False, [])
            result.append(Color(value))
        return DTOResult(False, result)
