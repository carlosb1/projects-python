import pytest
from pathlib import Path

from exer_user_link.domains import Token, User, SharedLink
from exer_user_link.adapters.repositories import TokenRepository, UserRepository
from exer_user_link.adapters.repositories import SharedLinkRepository


@pytest.fixture
def token_repository():
    return TokenRepository()


@pytest.fixture
def user_repository():
    return UserRepository()


@pytest.fixture
def sharedlink_repository():
    return SharedLinkRepository()


def test_should_save_token_correctly(token_repository):
    token = Token(userid="1")
    token_repository.save(token)
    assert(token_repository.find_by_value(token.value) is not None)


def test_should_remove_token_correctly(token_repository):
    token = Token(userid="1")
    token_repository.save(token)
    token_repository.remove(token)
    assert(token_repository.find_by_value(token.value) is None)


def test_should_find_token_and_not_found(token_repository):
    token = Token(userid="1")
    token_repository.save(token)
    assert(token_repository.find_by_value('0') is None)


def test_should_save_user_correctly(user_repository):
    user = User('user', 'password', [])
    user_repository.save(user)
    assert(user_repository.find_by_userid('user') is not None)


def test_should_find_user_and_not_found(user_repository):
    user = User('user', 'password', [])
    user_repository.save(user)
    assert(user_repository.find_by_userid('user2') is None)


def test_should_save_sharedlink_correctly(sharedlink_repository):
    shared_link = SharedLink('1', Path('/'))
    sharedlink_repository.save(shared_link)
    assert(sharedlink_repository.find_by_name_id(shared_link.name_id) is not None)


def test_should_update_sharedlink_correctly(sharedlink_repository):
    shared_link = SharedLink('1', Path('/'))
    sharedlink_repository.save(shared_link)
    sharedlink_repository.update(shared_link)
    assert(sharedlink_repository.find_by_name_id(shared_link.name_id) is not None)


def test_should_remove_sharedlink_correctly(sharedlink_repository):
    shared_link = SharedLink('1', Path('/'))
    sharedlink_repository.save(shared_link)
    sharedlink_repository.remove(shared_link)
    assert(sharedlink_repository.find_by_name_id(shared_link.name_id) is None)


def test_should_find_sharedlink_and_not_found(sharedlink_repository):
    shared_link = SharedLink('1', Path('/'))
    sharedlink_repository.save(shared_link)
    assert(sharedlink_repository.find_by_name_id('0') is None)
