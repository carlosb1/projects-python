import pytest
import datetime

from pathlib import Path

from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.domains import FileInfo, User
from exer_user_link.services.download_service import DownloadService, QUOTA_SIZE, Result


@pytest.fixture
def user_repository():
    return UserRepository()


def test_should_download_file_correctly(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    file_info = FileInfo(path_to_download.name, path_to_download)
    user = User('user', 'password', [file_info])
    user_repository.save(user)
    assert(download_service.run('user', file_info.name_id) == file_info.fil)


def test_should_not_download_file_if_user_not_exist(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    user_repository.save(
        User('user', 'password', [FileInfo(path_to_download.name, path_to_download)]))
    assert(download_service.run('user1', path_to_download) is Result.NOT_FOUND)


def test_should_not_download_file_if_file_not_exist(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    incorrect_path_to_download = Path('test1.file')
    user_repository.save(
        User('user', 'password', [FileInfo(path_to_download.name, incorrect_path_to_download)]))
    assert(download_service.run('user', path_to_download) is Result.NOT_FOUND)


def test_should_not_download_if_quota_is_exceeded(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    file_info = FileInfo(path_to_download.name, path_to_download)
    user = User('user', 'password', [file_info])
    user.limit_quota = True
    user.last_update_quota = datetime.datetime.now()
    user_repository.save(user)
    assert(download_service.run('user', file_info.name_id) is Result.QUOTA_LIMIT)


def test_should_download_if_quota_is_resetted(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    file_info = FileInfo(path_to_download.name, path_to_download)
    user = User('user', 'password', [file_info])
    user.limit_quota = True
    user.last_update_quota = datetime.datetime.now() - datetime.timedelta(minutes=6)
    user_repository.save(user)
    assert(download_service.run('user', file_info.name_id) == file_info.fil)


def test_should_restore_quota_when_it_is_exceeded(user_repository):
    download_service = DownloadService(user_repository)
    path_to_download = Path('test.file')
    file_info = FileInfo(path_to_download.name, path_to_download)
    user = User('user', 'password', [file_info])
    user_repository.save(user)
    user.limit_quota = False
    user.quota_in_bytes = -1.
    assert(download_service.run('user', file_info.name_id) is Result.QUOTA_LIMIT)
    user.last_update_quota = datetime.datetime.now() - datetime.timedelta(minutes=6)
    assert(download_service.run('user', file_info.name_id) == file_info.fil)
    assert(user_repository.find_by_userid('user').quota_in_bytes == QUOTA_SIZE)
