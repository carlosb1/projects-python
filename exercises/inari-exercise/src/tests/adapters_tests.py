import pytest
from adapters import RandomGeneratorAdapter


def test_should_create_a_result_correctly():
    from models import Color
    generator = RandomGeneratorAdapter(list(Color), 4)
    values = generator.generate()
    assert(len(values) == 4)
    assert(all(type(v) == Color for v in values))


def test_should_throws_error_not_correct_values():
    with pytest.raises(ValueError):
        assert(RandomGeneratorAdapter([], 4))


def test_should_throws_error_not_correct_siz():
    from models import Color
    with pytest.raises(ValueError):
        assert(RandomGeneratorAdapter(list(Color), 0))
