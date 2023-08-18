from exer_search_file.adapters.file_loader import FileLoader

from pathlib import Path


def test_cli_should_return_read_folder_correctly():
    file_loader = FileLoader()
    found_files = file_loader.load(Path('resources/test'))
    assert len(found_files) == 1
    values = found_files[list(found_files.keys())[0]]
    assert(values == ['example', 'test2', 'test3'])


def test_cli_should_return_read_folder_empty():
    file_loader = FileLoader()
    found_files = file_loader.load(Path('resources/test2'))
    assert len(found_files) == 0
