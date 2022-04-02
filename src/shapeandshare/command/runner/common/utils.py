""" Helpers """

import shutil
from pathlib import Path

from ..contacts.errors.unknown_argument_error import UnknownArgumentError


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


def init_environment_argument_parser(arguments: list[str]) -> bool:
    """
    `init` subcommand argument parser.

    Parameters
    ----------
    arguments: the arguments

    Returns
    -------
    boolean for `force` the only supported argument.
    """

    force: bool = False
    if len(arguments) == 1:
        if arguments[0] == "--force":
            force = True
        else:
            raise UnknownArgumentError(command="init", message="Only one argument `--force` is supported.")
    elif len(arguments) > 1:
        raise UnknownArgumentError(command="init", message="Only one argument `--force` is supported.")
    return force
