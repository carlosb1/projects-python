import pytest
from unittest.mock import patch
import app

from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@patch('builtins.input', lambda *args: 'hello world')
def test_cli_should_return_correct_values(runner):
    result = runner.invoke(app.main)
    assert result.output.strip().replace(' ', '') == (
        'resources/files/fil3:50%\nresources/files/fil2:50%\nresources/files/subcarpet/fil1:100%')
