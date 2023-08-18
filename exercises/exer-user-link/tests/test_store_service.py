import pytest

from unittest.mock import MagicMock
from pathlib import Path
from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.adapters.filemanager import FileManagerAdapter
from exer_user_link.services.store_service import StoreService
from exer_user_link.domains import User, FileInfo


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def file_manager():
    return FileManagerAdapter(Path('.'))


def test_should_store_files_correctly(user_repository, file_manager):
    store_service = StoreService(user_repository, file_manager)
    file_manager.save = MagicMock()
    path_to_store = Path('test.file')
    user_repository.save(
        User('user', 'password', [FileInfo(path_to_store.name, path_to_store)]))
    store_service.run('user', path_to_store)
    assert(len(user_repository.find_by_userid('user').files) == 2)
    assert(file_manager.save.called)


def test_should_not_store_files_if_user_not_exist(user_repository, file_manager):
    store_service = StoreService(user_repository, file_manager)
    file_manager.save = MagicMock()
    path_to_store = Path('test.file')
    user_repository.save(
        User('user', 'password', [FileInfo(path_to_store.name, path_to_store)]))
    assert(store_service.run('user1', path_to_store) is None)


def test_should_store_files_and_remove_old_video(user_repository, file_manager):
    store_service = StoreService(user_repository, file_manager)
    file_manager.save = MagicMock()
    file_manager.remove = MagicMock()
    path_to_store = Path('test.file')
    user_repository.save(
        User('user', 'password', [FileInfo(Path('test.file' + str(i)).name,
                                           Path('test.file' + str(i))) for i in range(99)]))
    assert(store_service.run('user', path_to_store) is not None)
    assert(user_repository.find_by_userid('user').files[0].name == 'test.file1')
    assert(user_repository.find_by_userid('user').files[-1].name == 'test.file')
