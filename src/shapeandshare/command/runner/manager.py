""" Command Runner Manger Definition """

import configparser
import logging
import sys
from pathlib import Path
from typing import Optional, Union

from .backends.backend_config import BackendConfig
from .backends.backend_factory import BackendFactory
from .backends.backend_package import BackendPackage
from .contacts.command_type import CommandType
from .contacts.dtos.manager.manager_config import ManagerConfig
from .contacts.errors.parse_error import ParseError
from .contacts.errors.unknown_argument_error import UnknownArgumentError
from .contacts.errors.unknown_command_error import UnknownCommandError

# Global Defaults
DEFAULT_CONFIG_FILE: str = ".bcrrc"
DEFAULT_CONFIG_PATH: Path = Path(".")
DEFAULT_COMMAND_TIMEOUT: int = 60  # In seconds
DEFAULT_CONFIG_TYPE: str = "config"


class Manager:
    """
    Command Runner Manger

    Attributes
    ----------
    backend
        Backend for use within this manager installation.
    settings
        Manager settings configuration.
    """

    backend: Union[BackendConfig, BackendPackage]
    settings: ManagerConfig

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

        if not config_file:
            config_file = DEFAULT_CONFIG_FILE
        if not base_path:
            base_path: Path = DEFAULT_CONFIG_PATH
        self.settings = Manager._load_configuration(config_file=(base_path / config_file))
        self.backend = BackendFactory.build(backend_type=self.settings.config.type)

    @staticmethod
    def _load_configuration(config_file: Path) -> ManagerConfig:
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
        config_partial: dict = {"command": {"timout": DEFAULT_COMMAND_TIMEOUT}, "config": {"type": DEFAULT_CONFIG_TYPE}}

        # Attempt to load
        if config_file.exists():
            if config_file.is_file():
                # load file..
                logging.getLogger(__name__).debug(f"Loading config file: {config_file.resolve().as_posix()}")
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
                    f"[SKIPPING] Config file load - Was not a file? {config_file.resolve().as_posix()}"
                )
        else:
            logging.getLogger(__name__).debug(
                f"[SKIPPING] Config file load - Does not exist: {config_file.resolve().as_posix()}"
            )

        return ManagerConfig.parse_obj(config_partial)

    def main(self) -> None:
        """Main entry point for the processing of the cli command."""

        try:
            self._process()
        except (UnknownCommandError, UnknownArgumentError, ParseError) as error:
            # Known Errors
            logging.getLogger(__name__).debug(str(error))
            print(str(error))
        except Exception as error:
            # We encountered an unhandled exception.  This shouldn't happen.
            print("---- Unhandled Exception ----")
            logging.getLogger(__name__).debug(str(error))
            print(str(error))
        Manager.display_generic_help()

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
            self.backend.initial_environment(arguments=arguments)
        elif subcommand == CommandType.RUN:
            self.backend.run_command(arguments=arguments, per_command_timeout=self.settings.command.timeout)
        else:
            raise UnknownCommandError(f"Unknown command {subcommand}")

    @staticmethod
    def display_generic_help() -> None:
        """Print out summary help"""
        summary: str = "Usage: bcr <command>\n" "\n" "where <command> is one of:\n" "help, init, run"
        print(summary)

    @staticmethod
    def display_full_help():
        """Print our full help"""
        Manager.display_generic_help()
