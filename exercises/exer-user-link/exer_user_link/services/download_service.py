"""Service to get files to be download."""
import datetime
import os
import logging
from pathlib import Path
from typing import Union
from enum import Enum

from exer_user_link.adapters.repositories import UserRepository
from exer_user_link.domains import QUOTA_SIZE
from exer_user_link.utils import find_in_file_info_by_name_id


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Result(Enum):
    """Result types."""
    NOT_FOUND = 0
    QUOTA_LIMIT = 1


class DownloadService():
    """Class for download files."""

    def __init__(self, user_repository: UserRepository, file_path: Path = Path('.')):
        self._user_repository = user_repository
        self._file_path = file_path

    def run(self, user_id: str, file_id: str) -> Union[Result, Path]:
        """Run service to verify it can be download file."""
        logger.info(f'Download file for {user_id} and fileid  {file_id}')
        user = self._user_repository.find_by_userid(user_id)
        if not user:
            return Result.NOT_FOUND

        # verify quota state
        if user.limit_quota:
            logger.info('Check your quota exceeded')
            # if you exceed quota check if it keep happens.
            if (datetime.datetime.now() - user.last_update_quota) < datetime.timedelta(minutes=5):
                logger.info('It is blocked 5 mins')
                return Result.QUOTA_LIMIT
            user.last_update_quota = datetime.datetime(1, 1, 1)
            user.limit_quota = False
            user.quota_in_bytes = QUOTA_SIZE

        # check current quota
        if user.quota_in_bytes <= 0.:
            logger.info('Check your quota of bytes')
            user.limit_quota = True
            user.last_update_quota = datetime.datetime.now()
            return Result.QUOTA_LIMIT

        try:
            logger.info(f'Check in your files by file_id {file_id}')
            index = find_in_file_info_by_name_id(user.files, file_id)
            if index == -1:
                return Result.NOT_FOUND
            fil_info = user.files[index]
            siz_in_bytes = os.path.getsize(str(self._file_path / fil_info.fil))
            logger.info(
                f'Updating quota: bytes to substract {siz_in_bytes} from {user.quota_in_bytes}')
            user.quota_in_bytes -= siz_in_bytes
            return fil_info.fil
        except ValueError as e:
            logger.critical(e, exc_info=True)
        return Result.NOT_FOUND
