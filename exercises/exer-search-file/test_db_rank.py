from exer_search_file.adapters.db_rank import DBRanking
from pathlib import Path


def test_it_should_save_and_find_correctly_a_value():
    db_rank = DBRanking()

    info_data = ['file', 'test']
    db_rank.save(Path('file.txt'), info_data)
    results = db_rank.query_by_word('test')
    assert (results == [Path('file.txt')])


def test_it_should_not_found_correctly_a_value():
    db_rank = DBRanking()
    info_data = ['file', 'test']
    db_rank.save(Path('file.txt'), info_data)
    results = db_rank.query_by_word('nofile')
    assert (len(results) == 0)
