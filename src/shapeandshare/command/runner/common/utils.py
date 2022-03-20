""" Helpers """

import shutil
from pathlib import Path


def clean(arguments: list[str]) -> None:
    """
    Removes files, folders specified.

    Parameters
    ----------
    arguments: list of files and/or folders to remove.
    """

    for item in arguments:
        item_obj: Path = Path(item)
        if item_obj.exists():
            if item_obj.is_file():
                item_obj.unlink(missing_ok=True)
            else:
                # process as dir
                shutil.rmtree(path=item_obj.resolve().as_posix(), ignore_errors=True)
