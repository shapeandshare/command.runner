import configparser
import sys
from pathlib import Path
from typing import Optional, Union

from .backends.backend_factory import BackendFactory, BackendType
from .backends.backend_package import BackendPackage
from .contacts.command_type import CommandType
from .backends.backend_config import BackendConfig
from .contacts.errors.parse_error import ParseError
from .contacts.errors.unknown_argument_error import UnknownArgumentError
from .contacts.errors.unknown_command_error import UnknownCommandError


class Manager:

    config_file: str
    base_path: Path
    backend: Union[BackendConfig, BackendPackage]

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = ".bcrrc"
        if base_path:
            self.base_path: Path = Path(base_path)
        else:
            self.base_path: Path = Path(".")
        self.backend = self._load_backend()

    @property
    def conf(self) -> Path:
        return self.base_path / self.config_file

    def _load_backend(self) -> Union[BackendConfig, BackendPackage]:
        backend: str = "config"
        if self.conf.exists():
            if self.conf.is_file():
                # load file..
                config: configparser.ConfigParser = configparser.ConfigParser()
                config.read(self.conf.resolve().as_posix())
                try:
                    backend: str = config["config"]["backend"]
                except KeyError as error:
                    raise UnknownCommandError("Missing backend in config section") from error
            else:
                raise ParseError(f"{self.conf.resolve().as_posix()} exists but is not a file, expected a file")
        return BackendFactory.build(backend_type=BackendType(backend))

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
