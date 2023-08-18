"""Various tools."""
from typing import List
from exer_user_link.domains import FileInfo


def find_in_file_info(li: List[FileInfo], index_value) -> int:
    """Function for mapping."""
    return next((i for i, item in enumerate(li) if item.fil == index_value), -1)


def find_in_file_info_by_name_id(li: List[FileInfo], name_id) -> int:
    """Function for mapping."""
    return next((i for i, item in enumerate(li) if item.name_id == name_id), -1)
