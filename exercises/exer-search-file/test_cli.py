from unittest.mock import MagicMock, Mock, patch
from pathlib import Path
from exer_search_file.domain import Searcher, Loader
from exer_search_file.entrypoints.cli import CLI


@patch('builtins.input', lambda *args: 'text')
def test_cli_prompt_message_correctly():
    mocked_loader = Loader(MagicMock(), MagicMock())
    mocked_loader.run = Mock()
    mocked_searcher = Searcher(MagicMock())
    mocked_searcher.run = Mock()
    mocked_searcher.run.side_effect = [[]]
    cli = CLI(mocked_searcher, mocked_loader)
    cli.start('.')
    mocked_loader.run.assert_called_once_with(Path('.'))
    mocked_searcher.run.assert_called_once_with(['text'])
