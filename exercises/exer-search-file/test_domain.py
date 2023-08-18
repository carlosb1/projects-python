from unittest.mock import MagicMock, Mock
from pathlib import Path

from exer_search_file.adapters.db_rank import DBRanking
from exer_search_file.adapters.file_loader import FileLoader
from exer_search_file.domain import Loader, Searcher


def test_loader_should_save_correctly_path_db():
    mocked_db_ranking = DBRanking()
    mocked_db_ranking.save = MagicMock()
    mocked_file_loader = FileLoader()
    mocked_file_loader.load = MagicMock(return_value={'link': ['text']})
    loader = Loader(mocked_db_ranking, mocked_file_loader)
    loader.run(Path(''))
    mocked_db_ranking.save.assert_called_once_with('link', ['text'])


def test_searcher_should_query_correctly_empy():
    mocked_db_ranking = DBRanking()
    mocked_db_ranking.query_by_word = MagicMock(return_value=[])
    searcher = Searcher(mocked_db_ranking)
    found_values = searcher.run(['text'])
    assert found_values == []


def test_searcher_should_query_correctly():
    mocked_db_ranking = DBRanking()
    mocked_db_ranking.query_by_word = MagicMock(return_value=['link'])
    searcher = Searcher(mocked_db_ranking)
    found_values = searcher.run(['text'])
    assert found_values == [("link", 1.0)]


def test_searcher_should_query_correctly_top_10():
    mocked_db_ranking = DBRanking()
    mocked_results = ['link' + str(index) for index in range(0, 11)]
    mocked_db_ranking.query_by_word = MagicMock(return_value=mocked_results)
    searcher = Searcher(mocked_db_ranking)
    found_values = searcher.run(['text'])
    assert found_values == [("link0", 1.0), ("link1", 1.0), ("link2", 1.0),
                            ("link3", 1.0), ("link4", 1.0), ("link5", 1.0),
                            ("link6", 1.0), ("link7", 1.0), ("link8", 1.0),
                            ("link9", 1.0)]


def test_searcher_should_query_correctly_with_percentages():
    mocked_db_ranking = DBRanking()
    mocked_db_ranking.query_by_word = Mock()
    return_value = [['link', 'link2', 'link3'], ['link2', 'link3'], ['link3']]
    mocked_db_ranking.query_by_word.side_effect = return_value
    searcher = Searcher(mocked_db_ranking)
    found_values = searcher.run(['text', 'hello', 'world'])
    assert found_values == [("link", 1.0 / 3.), ("link2", 2.0 / 3.), ("link3", 1.0)]
