from pathlib import Path
from exer_user_link.domains import Token, FileInfo, User, SharedLink, QUOTA_SIZE


def test_should_create_token_correctly():
    token = Token(userid="1")
    assert(token.value is not None)
    assert(token.current_date is not None)
    assert(token.userid == "1")
    assert(token.uses == 0)


def test_should_create_file_info_correctly():
    file_info = FileInfo('1', Path('/'))
    assert(file_info.name == '1')
    assert(file_info.fil == Path('/'))


def test_should_create_shared_link_correctly():
    shared_link = SharedLink(Path('/'))
    assert(shared_link.name_id is not None)
    assert(shared_link.fil == Path('/'))


def test_should_create_user_correctly():
    user = User('user', 'password', [])
    assert(user.user == 'user')
    assert(user.password == 'password')
    assert(user.files == [])
    assert(user.limit_quota is False)
    assert(user.quota_in_bytes == QUOTA_SIZE)
    assert(user.last_update_quota is not None)
