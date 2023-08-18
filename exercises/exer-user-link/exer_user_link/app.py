"""Main entrypoint to run project."""
from pathlib import Path
from exer_user_link.adapters.repositories import UserRepository, TokenRepository
from exer_user_link.adapters.repositories import SharedLinkRepository
from exer_user_link.adapters.filemanager import FileManagerAdapter
from exer_user_link.domains import User

from exer_user_link.entrypoints.rest_files import RESTEndpoint

USERNAME = 'user_id'
PASSWORD = 'password'
PATH_SAVE_FILES = Path('./static/')


def main():
    """Entrypoint main."""
    user_repository = UserRepository()
    token_repository = TokenRepository()
    sharedlink_repository = SharedLinkRepository()
    file_manager = FileManagerAdapter(PATH_SAVE_FILES)

    user_repository.save(User(USERNAME, PASSWORD, []))
    rest_endpoint = RESTEndpoint(user_repository, token_repository,
                                 sharedlink_repository, file_manager, USERNAME, PATH_SAVE_FILES)

    app = rest_endpoint.create_app()
    app.run()


if __name__ == '__main__':
    main()
