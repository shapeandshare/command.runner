import configparser
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


class Manager:
    backend: Union[BackendConfig, BackendPackage]
    settings: ManagerConfig

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if not config_file:
            config_file = ".bcrrc"
        if not base_path:
            base_path: Path = Path(".")
        self.settings = Manager._load_configuration(config_file=(base_path / config_file))
        self.backend = self._load_backend()

    @staticmethod
    def _load_configuration(config_file: Path) -> ManagerConfig:
        config_partial: dict = {"command": {"timout": 60}, "config": {"type": "config"}}
        if config_file.exists():
            if config_file.is_file():
                # load file..
                config: configparser.ConfigParser = configparser.ConfigParser()
                config.read(config_file.resolve().as_posix())
                for section in config.sections():
                    if section not in config_partial:
                        config_partial[section] = {}
                    for (key, val) in config.items(section):
                        config_partial[section][key] = val
        return ManagerConfig.parse_obj(config_partial)

    def _load_backend(self) -> Union[BackendConfig, BackendPackage]:
        return BackendFactory.build(backend_type=(self.settings.config.type))

    def main(self) -> None:
        try:
            self.process()
        except UnknownCommandError as error:
            print(str(error))
            Manager.display_generic_help()
        except UnknownArgumentError as error:
            print(str(error))
        except ParseError as error:
            print(str(error))

    def process(self) -> None:
        argument_count: int = len(sys.argv)

        if argument_count == 1:
            Manager.display_generic_help()
        else:
            try:
                command: CommandType = CommandType(sys.argv[1])
                self.subcommand(subcommand=command, arguments=sys.argv[2:])
            except ValueError as error:
                raise UnknownCommandError(f"Unknown command {sys.argv[1]}") from error

    def subcommand(self, subcommand: CommandType, arguments=list[str]) -> None:
        # TODO this needs per_command_timeout..

        if subcommand == CommandType.HELP:
            Manager.display_full_help()
        elif subcommand == CommandType.INIT:
            self.backend.initial_environment(arguments=arguments)
        elif subcommand == CommandType.RUN:
            self.backend.run_command(arguments=arguments)
        else:
            # should not be possible to hit
            raise UnknownCommandError(f"Unknown command {subcommand}")

    @staticmethod
    def display_generic_help() -> None:
        summary: str = "Usage: bcr <command>\n" "\n" "where <command> is one of:\n" "help, init, run"
        print(summary)

    @staticmethod
    def display_full_help():
        """TODO: Update!"""
        Manager.display_generic_help()
