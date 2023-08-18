"""Service to save in files in our domain."""
import logging
from typing import Union
from werkzeug.datastructures import FileStorage
from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.adapters.filemanager import FileManagerAdapter
from exer_user_link.domains import FileInfo

MAXIM_FILES = 99

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class StoreService():
    """Class provides a function to store files."""

    def __init__(self, user_repository: UserRepository, file_manager: FileManagerAdapter):
        self._user_repository = user_repository
        self._file_manager = file_manager

    def run(self, user_id: str, fil: FileStorage) -> Union[None, FileInfo]:
        """Main function to use caste which save files locally."""
        # verify token!
        logger.info(f'Store files for {user_id} with path {fil}')

        user = self._user_repository.find_by_userid(user_id)
        if not user:
            return None
        if len(user.files) >= MAXIM_FILES:
            file_to_remove = user.files.pop(0)
            self._file_manager.remove(file_to_remove.fil)
        file_saved = self._file_manager.save(fil)
        file_info = FileInfo(name=fil.name, fil=file_saved)
        user.files.append(file_info)
        self._user_repository.update(user)
        return file_info
