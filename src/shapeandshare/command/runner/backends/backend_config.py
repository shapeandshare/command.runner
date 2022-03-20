""" Python Config File Backend"""

import configparser
import json
from typing import Optional, Union

from ..contacts.dtos.backend_model import BackendModel
from ..contacts.errors.unknown_argument_error import UnknownArgumentError
from .abstract_backend import AbstractBackend


class BackendConfig(AbstractBackend):
    """
    Python Config File Backend
    This backend handles interactions with Pythons native configparser format.

    Attributes
    ----------
    DEFAULT_CONFIG_FILE
        The default config file, default: "bcr.config"
    """

    DEFAULT_CONFIG_FILE: str = "bcr.config"

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        super().__init__(config_file=config_file, base_path=base_path)
        self.model = self._load_config()

    def init_environment(self, arguments: list[str]) -> None:
        if len(arguments) > 0:
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")

    def _load_config(self) -> BackendModel:
        """
        Builds the `scripts` data from a configparser config.

        Returns
        -------
        The Backend Model DTO.
        """

        model_partial: dict = {"scripts": {}}

        # Attempt to load
        if self.conf.exists():
            if self.conf.is_file():
                # load file..
                config: configparser.ConfigParser = configparser.ConfigParser(delimiters="=")
                config.read(self.conf.resolve().as_posix())

                # Process the sections
                for section in config.sections():
                    if section not in model_partial:
                        model_partial[section] = {}
                    for (key, val) in config.items(section):
                        commands: Union[list, str] = json.loads(val)
                        if isinstance(commands, str):
                            model_partial[section][key] = [commands]
                        else:
                            model_partial[section][key] = commands

        return BackendModel.parse_obj(model_partial)
