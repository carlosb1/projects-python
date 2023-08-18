import pytest

from pathlib import Path
from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.services.list_service import ListService
from exer_user_link.domains import User, FileInfo


@pytest.fixture
def user_repository():
    return UserRepository()


def test_should_list_files_correctly(user_repository):
    list_service = ListService(user_repository)
    path_to_store = Path('test.file')
    user_repository.save(
        User('user', 'password', [FileInfo(path_to_store.name, path_to_store)]))
    user = list_service.run('user')
    assert(user is not None)


def test_should_not_list_files_correctly(user_repository):
    list_service = ListService(user_repository)
    user = list_service.run('user')
    assert(user is None)
