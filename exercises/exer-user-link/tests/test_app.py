import io
from unittest.mock import MagicMock
from pathlib import Path
import pytest
from exer_user_link.adapters.repositories import UserRepository, TokenRepository
from exer_user_link.adapters.repositories import SharedLinkRepository
from exer_user_link.adapters.filemanager import FileManagerAdapter
from exer_user_link.domains import User, FileInfo, Token
from exer_user_link.entrypoints.rest_files import RESTEndpoint

USERNAME = 'user_id'
PATH_SAVE_FILES = Path('')


@pytest.fixture
def sharedlink_repository():
    return SharedLinkRepository()


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def token_repository():
    return TokenRepository()


@pytest.fixture
def file_manager():
    return FileManagerAdapter(PATH_SAVE_FILES)


def test_authentication_should_work_correctly(user_repository,
                                              token_repository, sharedlink_repository,
                                              file_manager):
    user_repository.save(User('user_id', 'password', []))
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.post('/auth/user_id/password')
        assert('token' in rv.get_json())
        assert(rv.status_code == 200)


def test_authentication_should_not_work_incorrect_password(user_repository,
                                                           token_repository, sharedlink_repository,
                                                           file_manager):
    user_repository.save(User('user_id', 'password', []))
    sharedlink_repository = SharedLinkRepository()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.post('/auth/user_id/wrongpassword')
        assert(rv.status_code == 400)


def test_list_should_fail_authentication_incorrect_token(user_repository,
                                                         token_repository, sharedlink_repository,
                                                         file_manager):
    user_repository.save(User('user_id', 'password', []))
    sharedlink_repository = SharedLinkRepository()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/me', headers={'Authorization': 'Bearer incorrectoken'})
        assert(rv.status_code == 401)


def test_list_should_work_correctly(user_repository,
                                    token_repository, sharedlink_repository,
                                    file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('./folder/test.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/me', headers={'Authorization': 'Bearer ' + token_value})
        assert(str(rv.get_json()) ==
               "{'files': [{'name': 'test.file', 'url': 'folder/test.file'}], 'user': 'user_id'}")
        assert(rv.status_code == 200)


def test_post_file_should_work_correctly(user_repository,
                                         token_repository, sharedlink_repository,
                                         file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('./folder/test.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        data = dict(file=(io.BytesIO(b'my file contents'), 'test.file'),)
        rv = client.post('/me', data=data, headers={'Authorization': 'Bearer ' + token_value})
        assert(rv.status_code == 200)


def test_file_should_fail_shared_unauthorized(user_repository,
                                              token_repository, sharedlink_repository,
                                              file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('./folder/test.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/' + 'test' + '/share',
                        headers={'Authorization': 'Bearer incorrecttoken'})
        assert(rv.status_code == 401)


def test_file_should_shared_file_correctly(user_repository,
                                           token_repository, sharedlink_repository,
                                           file_manager):
    file_info = FileInfo('test.file', Path('test.file'))
    user_repository.save(User('user_id', 'password', [file_info]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/' + str(file_info.name_id) + '/share',
                        headers={'Authorization': 'Bearer ' + token_value})

        assert('shared_url' in rv.get_json())
        assert(rv.status_code == 200)


def test_file_should_fail_not_found_correctly(user_repository,
                                              token_repository, sharedlink_repository,
                                              file_manager):

    file_info = FileInfo('test.file', Path('testnofound.file'))
    user_repository.save(User('user_id', 'password', [file_info]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/nofile/share',
                        headers={'Authorization': 'Bearer ' + token_value})

        assert(rv.status_code == 404)


def test_file_should_download_shared_file_correctly(user_repository,
                                                    token_repository, sharedlink_repository,
                                                    file_manager):
    file_info = FileInfo('test_to_upload.file', Path('test_to_upload.file'))
    user_repository.save(User('user_id', 'password', [file_info]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager,
                       USERNAME, Path('resources')).create_app()
    with app.test_client() as client:
        rv = client.get('/f/' + str(file_info.name_id) + '/share',
                        headers={'Authorization': 'Bearer ' + token_value})

        shared_link = rv.get_json()['shared_url']
        assert(rv.status_code == 200)
        rv = client.get(shared_link)
        assert(rv.status_code == 200)


def test_file_should_fail_download_shared_not_found_correctly(user_repository,
                                                              token_repository,
                                                              sharedlink_repository,
                                                              file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('testnofound.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/s/notexisyyt')
        assert(rv.status_code == 404)


def test_file_should_fail_download_unauthorized(user_repository,
                                                token_repository, sharedlink_repository,
                                                file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('./folder/test.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/' + 'noexist',
                        headers={'Authorization': 'Bearer incorrecttoken'})
        assert(rv.status_code == 401)


def test_file_should_fail_download_not_found_correctly(user_repository,
                                                       token_repository, sharedlink_repository,
                                                       file_manager):
    user_repository.save(User('user_id', 'password', [
                         FileInfo('test.file', Path('testnofound.file'))]))
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/notexisyyt',
                        headers={'Authorization': 'Bearer ' + token_value})
        assert(rv.status_code == 404)


def test_file_should_fail_download_quote_limit_correctly(user_repository,
                                                         token_repository, sharedlink_repository,
                                                         file_manager):

    user = User('user_id', 'password', [FileInfo('test.file', Path('./folder/test.file'))])
    user.limit_quota = False
    user.quota_in_bytes = -1.
    user_repository.save(user)
    token_value = 'correcttoken'
    token = Token(userid='user_id', value=token_value)
    token_repository.save(token)
    file_manager.save = MagicMock()
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/f/notexisyyt',
                        headers={'Authorization': 'Bearer ' + token_value})
        assert(rv.status_code == 429)


def test_should_run_404_not_resource(user_repository,
                                     token_repository, sharedlink_repository,
                                     file_manager):
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.post('/iamnotexist')
        assert(rv.status_code == 404)


def test_should_run_405_not_method(user_repository,
                                   token_repository, sharedlink_repository,
                                   file_manager):
    app = RESTEndpoint(user_repository, token_repository,
                       sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES).create_app()
    with app.test_client() as client:
        rv = client.get('/auth/user_id/password')
        assert(rv.status_code == 405)
