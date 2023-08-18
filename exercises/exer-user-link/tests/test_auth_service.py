import pytest
import datetime
from exer_user_link.adapters.repositories import TokenRepository, UserRepository
from exer_user_link.services.auth_service import AuthService
from exer_user_link.domains import User


@pytest.fixture
def token_repository():
    return TokenRepository()


@pytest.fixture
def user_repository():
    return UserRepository()


def test_should_create_a_correct_token(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    assert(generated_token is not None)
    assert(token_repository.find_by_value(generated_token.value) is not None)


def test_should_not_be_authenticated_with_incorrect_password(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'nopassword')
    assert(generated_token is None)


def test_not_should_create_token_for_incorrect_user(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user1', 'password')
    assert(generated_token is None)


def test_should_verify_a_correct_token(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    assert(auth_service.verify(generated_token) is True)


def test_should_verify_not_exist_token(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    generated_token.value = 'wrongtoken'
    assert(auth_service.verify(generated_token) is False)


def test_should_verify_not_correct_user(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    generated_token.userid = 'wronguser'
    assert(auth_service.verify(generated_token) is False)


def test_should_verify_old_token(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    # generate and modify token
    modified_token = token_repository.find_by_value(generated_token.value)
    modified_token.uses = 4
    token_repository.update(modified_token)
    auth_service.verify(generated_token)
    assert(token_repository.find_by_value(generated_token.value) is None)


def test_should_verify_it_is_used_too_much_times(token_repository, user_repository):
    auth_service = AuthService(token_repository, user_repository)
    user_repository.save(User('user', 'password', []))
    generated_token = auth_service.authenticate('user', 'password')
    # generate and modify token
    modified_token = token_repository.find_by_value(generated_token.value)
    modified_token.current_date -= datetime.timedelta(minutes=5)
    token_repository.update(modified_token)
    assert(auth_service.verify(generated_token) is False)
    assert(token_repository.find_by_value(generated_token.value) is None)
