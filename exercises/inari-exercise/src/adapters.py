import abc
import random


class GeneratorAdapter(abc.ABC):
    """
        Adapter contract to reuse for different adapters
    """
    @abc.abstractmethod
    def generate(self) -> list:
        return ""


class RandomGeneratorAdapter(GeneratorAdapter):
    """
        Adaptor to generate random values
    """
    def __init__(self, values, siz):
        if len(values) == 0:
            raise ValueError("It must be added a not empty list of values")
        if siz <= 0:
            raise ValueError("It must be added a siz greater than 0")
        self.values = values
        self.siz = siz

    def generate(self) -> list:
        return [random.choice(self.values) for x in range(0, self.siz)]
