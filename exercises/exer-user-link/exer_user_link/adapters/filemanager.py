"""Adapter service to manage files."""

from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


class FileManagerAdapter:
    """File manager adapter to save and removes files."""

    def __init__(self, path_files: Path):
        self._path_files = path_files
        if not path_files.exists():
            raise RuntimeError('Path to save files  doesn t exit')

    def save(self, fil: FileStorage) -> Path:
        """Save function."""
        filename = secure_filename(str(fil.filename))
        fil.save(str(self._path_files / filename))
        return Path(filename)

    def remove(self, fil: Path):
        """Remove function."""
        fil.unlink()
