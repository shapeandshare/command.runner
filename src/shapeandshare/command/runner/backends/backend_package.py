""" NPM package.json Config File Backend"""

from typing import Optional

from ..contacts.dtos.package import Package
from ..contacts.errors.unknown_argument_error import UnknownArgumentError
from .abstract_backend import AbstractBackend


class BackendPackage(AbstractBackend):
    """
    NPM package.json Config File Backend
    This backend handles interactions with NPM's native package.json file format.

    Attributes
    ----------
    DEFAULT_CONFIG_FILE
        The default config file, default: "package.json"
    """

    # Global Defaults
    DEFAULT_CONFIG_FILE: str = "package.json"

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        super().__init__(config_file=config_file, base_path=base_path)
        self.package = Package.parse_file(self.conf.resolve().as_posix())

    def init_environment(self, arguments: list[str]) -> None:
        if len(arguments) > 0:
            print(f"init_environment, Arguments: ({arguments})")
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")
        message: str = "Use: npm init" "For additional details see:" "https://docs.npmjs.com/cli/v8/using-npm/scripts"
        print(message)
