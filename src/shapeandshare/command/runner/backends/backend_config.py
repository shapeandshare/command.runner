import configparser
import json
from pathlib import Path
from typing import Optional, Union

from ..contacts.errors.parse_error import ParseError
from ..contacts.errors.unknown_argument_error import UnknownArgumentError
from ..contacts.errors.unknown_command_error import UnknownCommandError
from .abstract_backend import AbstractBackend


class BackendConfig(AbstractBackend):
    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "bcr.config"
        if base_path:
            self.base_path: Path = Path(base_path)
        else:
            self.base_path: Path = Path(".")

    def initial_environment(self, arguments: list[str]) -> None:
        if len(arguments) > 0:
            print(f"initial_environment, Arguments: ({arguments})")
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")

        config: configparser.ConfigParser = configparser.ConfigParser()
        config.read(self.conf.resolve().as_posix())
        # config["scripts"] = {"asd:asd": "asd"}
        with open(self.conf.resolve().as_posix(), mode="w", encoding="utf-8") as configfile:
            config.write(configfile)

    def run_command(self, arguments: list[str]) -> None:
        # print(f"run_command, Arguments: ({arguments})")
        if len(arguments) == 0:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")
        config: configparser.ConfigParser = configparser.ConfigParser()
        config.read(self.conf.resolve().as_posix())
        try:
            raw_commands: Union[list, str] = json.loads(config["scripts"][arguments[0]])
            # print(f"raw_commands: ({raw_commands})")
        except KeyError as error:
            raise UnknownCommandError(f"Unknown command {arguments[0]} in [scripts]") from error
        except json.JSONDecodeError as error:
            raise ParseError(f"Unable to load [script] {arguments[0]}.  It was not JSON parsable.") from error

        # If given a single string then drop it into a list.
        commands: list = []
        if isinstance(raw_commands, str):
            commands.append(raw_commands)
        else:
            commands = raw_commands

        # Command executor
        BackendConfig._command_executor(commands=commands, shell=True)
