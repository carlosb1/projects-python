import pytest
from pathlib import Path

from werkzeug.datastructures import FileStorage
from exer_user_link.adapters.filemanager import FileManagerAdapter


def test_should_create_and_remove_correctly():
    file_manager_adapter = FileManagerAdapter(Path('./'))
    tested_file_path = Path('file.test')
    _ = open(tested_file_path, 'w').close()
    fp = open(tested_file_path, 'r')
    fil_storage = FileStorage(fp)
    fil_storage.filename = 'file2.test'
    result_filename = file_manager_adapter.save(fil_storage)
    assert(result_filename.exists() is True)
    file_manager_adapter.remove(result_filename)
    assert(result_filename.exists() is False)
    tested_file_path.unlink()


def test_should_not_start_service_with_incorrect_path():
    with pytest.raises(RuntimeError):
        _ = FileManagerAdapter(Path('./noexist'))
