"""Authentication and authorization process."""
import datetime
import logging
from exer_user_link.adapters.repositories import TokenRepository, UserRepository
from exer_user_link.domains import Token
from typing import Union

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthService():
    """Auth service to generate and verify tokens."""

    def __init__(self, token_repository: TokenRepository, user_repository: UserRepository):
        self._token_repository = token_repository
        self._user_repository = user_repository

    def authenticate(self, user_id: str, password: str) -> Union[None, Token]:
        """Authentication function."""
        logger.info(f'Authentication {user_id}')
        user = self._user_repository.find_by_userid(user_id)
        if not user:
            return None
        if user.password != password:
            return None
        token_value = self._generate_new_token(user_id)
        return Token(userid=user_id, value=token_value)

    def verify(self, token: Token) -> bool:
        """Verificationfunction."""
        logger.info(f'Verifying {str(token.value)}')
        restored_token = self._token_repository.find_by_value(token.value)
        if not restored_token:
            return False
        if not restored_token.userid == token.userid:
            return False
        if (datetime.datetime.now() - restored_token.current_date) >= datetime.timedelta(minutes=5):
            self._token_repository.remove(restored_token)
            return False
        restored_token.uses += 1
        # avoid magic number
        if restored_token.uses < 5:
            self._token_repository.update(restored_token)
        else:
            # correct token but removed from the db.
            self._token_repository.remove(restored_token)
        return True

    def _generate_new_token(self, user_id: str) -> str:
        token = Token(user_id)
        self._token_repository.save(token)
        return token.value
