"""REST endpoint class."""
from pathlib import Path
from typing import Union
import logging
from flask import Flask, send_from_directory, request
import flask

from exer_user_link.adapters.repositories import UserRepository, TokenRepository
from exer_user_link.adapters.repositories import SharedLinkRepository
from exer_user_link.adapters.filemanager import FileManagerAdapter
from exer_user_link.services.auth_service import AuthService
from exer_user_link.services.list_service import ListService
from exer_user_link.services.store_service import StoreService
from exer_user_link.services.sharelink_service import ShareLinkService
from exer_user_link.services.download_service import DownloadService, Result
from exer_user_link.domains import Token
from exer_user_link.entrypoints.factory_responses import FactoryResponse


PREFIX_SHARED = '/s/'
PREFIX_PRIVATE = '/f/'


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RESTEndpoint:
    """Rest endpoint class to manage links."""

    def __init__(self, user_repository: UserRepository,
                 token_repository: TokenRepository,
                 sharedlink_repository: SharedLinkRepository,
                 file_manager: FileManagerAdapter,
                 username: str,
                 path_save: Path
                 ):
        self._user_repository = user_repository
        self._token_repository = token_repository
        self._sharedlink_repository = sharedlink_repository
        self._file_manager = file_manager
        self._response_factory = FactoryResponse()
        self._username = username
        self._path_save = path_save

    def create_app(self):
        """Builder function for creating app."""
        app = Flask(__name__, static_folder=str(self._path_save))

        def _extract_token() -> Union[None, str]:
            auth_header = request.headers['Authorization']
            if not auth_header.startswith("Bearer "):
                return None

            return auth_header[7:]

        def _validation() -> bool:
            logger.info('Validating token...')
            token_value = _extract_token()
            logger.info(f'Extracting token {token_value}')
            if not token_value:
                return False
            validation = AuthService(self._token_repository,
                                     self._user_repository).verify(
                Token(userid=self._username, value=token_value))

            logger.info(f'Validated token:{validation}')
            if not validation:
                return False
            return True

        @app.route('/auth/<userid>/<password>', methods=['POST'])
        def auth(userid: str, password: str):
            """Endpoint to authenticate and response token."""
            logger.info(f'Authenticating user {userid} and password')
            token = AuthService(self._token_repository,
                                self._user_repository).authenticate(userid, password)
            if token:
                return self._response_factory.new200({'token': token.value})
            else:
                return self._response_factory.new400()
                # set up response.

        @ app.route('/me', methods=['GET'])
        def list():
            """List files from user."""
            logger.info(f'Listing files from user {self._username}')
            is_valid = _validation()
            if not is_valid:
                return self._response_factory.new401()

            user = ListService(self._user_repository).run(self._username)
            files = [{'name': fil.name, 'url': str(fil.fil)} for fil in user.files]
            data = {'user': self._username, 'files': files}

            return self._response_factory.new200(data)

        @ app.route('/me', methods=['POST'])
        def upload():
            """Upload file endpoint."""
            logger.info('Uploading file.')
            is_valid = _validation()
            if not is_valid:
                return self._response_factory.new401()
            file = request.files['file']
            # FIXME It can happens, some internal error saving infor.
            file_info = StoreService(self._user_repository,
                                     self._file_manager).run(self._username, file)

            # TODO move this respons.
            data = {}
            if file_info:
                data = {'name': file_info.name, 'url': PREFIX_PRIVATE + file_info.name_id}

            return self._response_factory.new200(data)

        @ app.route('/f/<file_id>/share', methods=['GET'])
        def create_share_link(file_id: str):
            """Create share link endpoint."""
            logger.info(f'Create shared file for {file_id}')
            is_valid = _validation()
            if not is_valid:
                return self._response_factory.new401()
            shared_link = ShareLinkService(
                self._user_repository,
                self._sharedlink_repository).generate_link(self._username, file_id)
            if not shared_link:
                return self._response_factory.new404()

            return self._response_factory.new200({'shared_url': PREFIX_SHARED + shared_link})

        @ app.route('/f/<file_id>', methods=['GET'])
        def download(file_id: str):
            """Download private file."""
            logger.info(f'Download private file for {file_id}')
            is_valid = _validation()
            if not is_valid:
                return self._response_factory.new401()

            filename = DownloadService(self._user_repository,
                                       self._path_save).run(self._username, file_id)

            logger.info(f'Return filename {filename}')
            if filename == Result.NOT_FOUND:
                return self._response_factory.new404()
            if filename == Result.QUOTA_LIMIT:
                return self._response_factory.new429()

            path_to_load = str(Path(flask.helpers.get_root_path(
                str(self._path_save))) / self._path_save)
            logger.info(f'Trying to download file {filename} from direc {path_to_load}')

            return send_from_directory(str(path_to_load),
                                       str(filename), as_attachment=True)

        @ app.route('/s/<file_id>', methods=['GET'])
        def download_share(file_id: str):
            """Download shared file."""
            logger.info(f'Download shared file for {file_id}')
            filename = ShareLinkService(
                self._user_repository,
                self._sharedlink_repository).download_link(file_id)
            logger.info(f'Return filename {filename}')
            if not filename:
                return self._response_factory.new404()

            path_to_load = str(Path(flask.helpers.get_root_path(
                str(self._path_save))) / self._path_save)
            logger.info(f'Trying to download file {filename} from direc {path_to_load}')
            # check it it is shared
            return send_from_directory(str(path_to_load),
                                       str(filename), as_attachment=True)

        @ app.errorhandler(404)
        def resource_not_found(e):
            return self._response_factory.new404(str(e))

        return app
