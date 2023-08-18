"""Adapter file. It manages operatiom with the filesystem."""
from typing import Dict, List
from pathlib import Path


class FileLoader:
    """Class responsible to manage how we load files."""

    def load(self, path_file: Path) -> Dict[str, List[str]]:
        """Load function from a path file.

        This path is a directory and subdirectories to find files.

        Args:
            path_file (Path): path of the directory to look over

        Returns:
            Dict: dictionary with filename (key) and its words (value)

        """
        loaded_info = dict()
        for filename in path_file.rglob("*"):
            if filename.is_dir():
                continue
            with open(filename) as file:
                loaded_info[str(filename)] = file.read().replace("\n", "").split(" ")
        return loaded_info
