""" Python Config File Backend"""

import configparser
import json
from typing import Optional, Union

from ..common.utils import init_environment_argument_parser
from ..contacts.dtos.backend_model import BackendModel
from .abstract_backend import AbstractBackend


class BackendConfig(AbstractBackend):
    """
    Python Config File Backend
    This backend handles interactions with Pythons native configparser format.

    Attributes
    ----------
    DEFAULT_CONFIG_FILE
        The default config file, default: "sacr.config"
    """

    DEFAULT_CONFIG_FILE: str = "sacr.config"

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        super().__init__(config_file=config_file, base_path=base_path)
        self.model = self._load_config()

    def init_environment(self, arguments: list[str]) -> None:
        force: bool = init_environment_argument_parser(arguments=arguments)

        if self.conf.exists() and force or not self.conf.exists():
            # write default config
            new_config: configparser.ConfigParser = configparser.ConfigParser(delimiters="=")
            new_config.add_section(section="scripts")
            new_config.set(section="scripts", option="hello", value='"echo hello"')

            with open(self.conf.resolve().as_posix(), mode="w", encoding="utf-8") as file:
                new_config.write(file)
            print(f"Sample config created at: {self.conf.resolve().as_posix()}")
        else:
            message: str = (
                f"A configuration file already exists at {self.conf.resolve()}. To over-ride use `--force` flag."
            )
            print(message)

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
