"""Domain classes. They represent the domain entities."""
from typing import List
from dataclasses import dataclass
from pathlib import Path
import uuid
import random
import datetime

QUOTA_SIZE = 1024 * 1024 * 5


def generate() -> str:
    """Function to generate token values."""
    rd = random.Random()
    rd.seed(datetime.datetime.now())
    token_value = str(uuid.UUID(int=rd.getrandbits(128)))
    return token_value


@ dataclass
class Token:
    """Token entity."""
    userid: str
    value: str = generate()
    current_date: datetime.datetime = datetime.datetime.now()
    uses: int = 0


@ dataclass
class FileInfo:
    """FileInfo entity."""
    name: str
    fil: Path
    name_id: str = str(uuid.uuid4())[:13]


@ dataclass
class SharedLink:
    """Shared link."""
    fil: Path
    name_id: str = str(uuid.uuid4())[:13]


@ dataclass
class User:
    """User entity."""
    user: str
    password: str
    files: List[FileInfo]
    limit_quota: bool = False
    quota_in_bytes: int = QUOTA_SIZE
    last_update_quota: datetime.datetime = datetime.datetime.now()
