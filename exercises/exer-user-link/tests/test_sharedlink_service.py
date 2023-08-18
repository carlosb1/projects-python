import pytest
from pathlib import Path
from exer_user_link.adapters.repositories import SharedLinkRepository, UserRepository
from exer_user_link.services.sharelink_service import ShareLinkService
from exer_user_link.domains import User, FileInfo


@pytest.fixture
def sharedlink_repository():
    return SharedLinkRepository()


@pytest.fixture
def user_repository():
    return UserRepository()


def test_should_create_a_correct_link(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    path_to_generate = Path('test.file')
    file_info = FileInfo(path_to_generate.name, path_to_generate)
    user_repository.save(
        User('user', 'password', [file_info]))
    generated_link = sharelink_service.generate_link('user', file_info.name_id)
    assert(generated_link is not None)


def test_should_not_create_link_for_incorrect_user(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    path_to_generate = Path('test.file')
    file_info = FileInfo(path_to_generate.name, path_to_generate)
    user_repository.save(
        User('user', 'password', [file_info]))
    generated_link = sharelink_service.generate_link('user1', file_info.name_id)
    assert(generated_link is None)


def test_should_not_create_link_for_user_without_list(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    user_repository.save(
        User('user', 'password', []))
    generated_link = sharelink_service.generate_link('user', 'id')
    assert(generated_link is None)


def test_should_download_link(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    path_to_generate = Path('test.file')
    file_info = FileInfo(path_to_generate.name, path_to_generate)
    user_repository.save(
        User('user', 'password', [file_info]))
    generated_link = sharelink_service.generate_link('user', file_info.name_id)
    assert(sharelink_service.download_link(generated_link) is not None)


def test_should_generate_link(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    path_to_generate = Path('test.file')
    file_info = FileInfo(path_to_generate.name, path_to_generate)
    user_repository.save(
        User('user', 'password', [file_info]))
    generated_link = sharelink_service.generate_link('user', file_info.name_id)
    assert(sharelink_service.download_link(generated_link) is not None)


def test_should_generate_link_if_not_exist(sharedlink_repository, user_repository):
    sharelink_service = ShareLinkService(user_repository, sharedlink_repository)
    path_to_generate = Path('test.file')
    file_info = FileInfo(path_to_generate.name, path_to_generate)
    user_repository.save(
        User('user', 'password', [file_info]))
    sharelink_service.generate_link('user', file_info.name_id)
    assert(sharelink_service.download_link('notexist') is None)
