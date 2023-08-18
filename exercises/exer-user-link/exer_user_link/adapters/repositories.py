"""Repositories to save information."""
from typing import Union
from exer_user_link.domains import Token, User, SharedLink


class TokenRepository:
    """In memory repository to manage tokens."""

    def __init__(self):
        self.table = dict()

    def save(self, token: Token):
        """Save token."""
        self.table[token.value] = token

    def update(self, token: Token):
        """Update token."""
        self.table[token.value] = token

    def remove(self, token: Token):
        """Remove token."""
        del self.table[token.value]

    def find_by_value(self, token_value: str) -> Union[None, Token]:
        """Find token by value."""
        if token_value in self.table:
            return self.table[token_value]
        else:
            return None


class UserRepository:
    """In memory repository to manage users."""

    def __init__(self):
        self.table = dict()

    def save(self, user: User):
        """Save user."""
        self.table[user.user] = user

    def update(self, user: User):
        """Update user."""
        self.table[user.user] = user

    def find_by_userid(self, user_id: str) -> Union[None, User]:
        """Find User by userid."""
        if user_id in self.table:
            return self.table[user_id]
        else:
            return None


class SharedLinkRepository:
    """In memory repository to manage shared links."""

    def __init__(self):
        self.table = dict()

    def save(self, sharedlink: SharedLink):
        """Save shared link."""
        self.table[sharedlink.name_id] = sharedlink

    def update(self, sharedlink: SharedLink):
        """Update shared link."""
        self.table[sharedlink.name_id] = sharedlink

    def remove(self, sharedlink: SharedLink):
        """Remove sharedlink."""
        del self.table[sharedlink.name_id]

    def find_by_name_id(self, name_id: str) -> Union[None, SharedLink]:
        """Find sharedlink by name_id."""
        if name_id in self.table:
            return self.table[name_id]
        else:
            return None
