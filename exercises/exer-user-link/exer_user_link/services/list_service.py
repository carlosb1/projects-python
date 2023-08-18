"""Service to list files in our domain."""
import logging
from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.domains import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ListService():
    """Class provides a function to store files."""

    def __init__(self, user_repository: UserRepository):
        self._user_repository = user_repository

    def run(self, user_id: str) -> User:
        """Main function to use caste which list files."""
        logger.info(f'Listing user info for {user_id}')
        user = self._user_repository.find_by_userid(user_id)
        if not user:
            return None
        return user
