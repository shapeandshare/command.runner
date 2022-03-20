""" Command Runner Manger Definition """

import configparser
import logging
import sys
from pathlib import Path
from typing import Optional, Union

from .backends.backend_config import BackendConfig
from .backends.backend_factory import BackendFactory
from .backends.backend_package import BackendPackage
from .common.utils import clean
from .contacts.command_type import CommandType
from .contacts.dtos.manager.manager_config import ManagerConfig
from .contacts.errors.parse_error import ParseError
from .contacts.errors.unknown_argument_error import UnknownArgumentError
from .contacts.errors.unknown_command_error import UnknownCommandError


class Manager:
    """
    Command Runner Manger

    Attributes
    ----------
    backend
        Backend for use within this manager installation.
    settings
        Manager settings configuration.
    DEFAULT_CONFIG_FILE
        The default config file to use for manager settings, default: ".sacrrc"
    DEFAULT_CONFIG_PATH
        The default location for the manager configuration file, default: Path(".")
    DEFAULT_COMMAND_TIMEOUT
        The default per command time out threshold, default: None (no timeout)
    DEFAULT_CONFIG_TYPE
        The default backend type, default: "config"
    """

    backend: Union[BackendConfig, BackendPackage]
    settings: ManagerConfig

    # Global Defaults
    DEFAULT_CONFIG_FILE: str = ".sacrrc"
    DEFAULT_CONFIG_PATH: Path = Path(".")
    DEFAULT_COMMAND_TIMEOUT: Optional[int] = None  # In seconds
    DEFAULT_CONFIG_TYPE: str = "config"

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        """
        Class Constractor

        Parameters
        ----------
        config_file
            The filename of the manager config file to load.
        base_path
            The local file system directory that the config file resides within.
        """

        if config_file is None:
            config_file = self.DEFAULT_CONFIG_FILE
        if base_path is None:
            base_path = self.DEFAULT_CONFIG_PATH
        else:
            base_path = Path(base_path)
        self.settings = self._load_configuration(config_file=(base_path / config_file))
        self.backend = BackendFactory.build(
            backend_type=self.settings.config.type,
            config_file=self.settings.config.file,
            base_path=self.settings.config.path,
        )

    def _load_configuration(self, config_file: Path) -> ManagerConfig:
        """
        Load Manager Configuration

        Parameters
        ----------
        config_file
            Path to for the local file system configuration file to load.

        Returns
        -------
            A ManagerConfig DTO for the configuration file.
        """

        # load the defaults
        config_partial: dict = {
            "command": {"timeout": self.DEFAULT_COMMAND_TIMEOUT},
            "config": {"type": self.DEFAULT_CONFIG_TYPE, "file": None, "path": None},
        }

        # Attempt to load
        if config_file.exists():
            if config_file.is_file():
                # load file..
                logging.getLogger(__name__).debug("Loading config file: {%s}", config_file.resolve().as_posix())
                config: configparser.ConfigParser = configparser.ConfigParser()
                config.read(config_file.resolve().as_posix())

                # Process the sections
                for section in config.sections():
                    if section not in config_partial:
                        config_partial[section] = {}
                    for (key, val) in config.items(section):
                        config_partial[section][key] = val
            else:
                logging.getLogger(__name__).warning(
                    "[SKIPPING] Config file load - Was not a file? {%s}", config_file.resolve().as_posix()
                )
        else:
            logging.getLogger(__name__).debug(
                "[SKIPPING] Config file load - Does not exist: {%s}", config_file.resolve().as_posix()
            )
        return ManagerConfig.parse_obj(config_partial)

    def main(self) -> None:
        """Main entry point for the processing of the cli command."""

        # pylint: disable=broad-except
        try:
            self._process()
        except (UnknownCommandError, UnknownArgumentError, ParseError) as error:
            # Known Errors
            logging.getLogger(__name__).debug(str(error))
            print(str(error))
            Manager.display_generic_help()
        except Exception as error:
            # We encountered an unhandled exception.  This shouldn't happen.
            print("---- Unhandled Exception ----")
            logging.getLogger(__name__).debug(str(error))
            print(str(error))
        # pylint: enable=broad-except

    def _process(self) -> None:
        """Process CLI Arguments"""

        argument_count: int = len(sys.argv)

        if argument_count == 1:
            Manager.display_generic_help()
        else:
            try:
                command: CommandType = CommandType(sys.argv[1])
                self._subcommand(subcommand=command, arguments=sys.argv[2:])
            except ValueError as error:
                raise UnknownCommandError(f"Unknown command {sys.argv[1]}") from error

    def _subcommand(self, subcommand: CommandType, arguments=list[str]) -> None:
        """Process the given subcommand"""

        if subcommand == CommandType.HELP:
            Manager.display_full_help()
        elif subcommand == CommandType.INIT:
            self.backend.init_environment(arguments=arguments)
        elif subcommand == CommandType.RUN:
            self.backend.run_command(arguments=arguments, per_command_timeout=self.settings.command.timeout)
        elif subcommand == CommandType.CLEAN:
            clean(arguments=arguments)
        else:
            raise UnknownCommandError(f"Unknown command {subcommand}")

    @staticmethod
    def display_generic_help() -> None:
        """Print out summary help"""
        summary: str = "Usage: sacr <command>\n" "\n" "where <command> is one of:\n" "help, init, run, clean"
        print(summary)

    @staticmethod
    def display_full_help():
        """Print our full help"""
        Manager.display_generic_help()
