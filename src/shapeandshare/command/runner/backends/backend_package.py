from pathlib import Path
from typing import Optional

from ..contacts.dtos.package import Package
from ..contacts.errors.unknown_argument_error import UnknownArgumentError
from ..contacts.errors.unknown_command_error import UnknownCommandError
from .abstract_backend import AbstractBackend


class BackendPackage(AbstractBackend):
    package: Package

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "package.json"
        if base_path:
            self.base_path: Path = Path(base_path)
        else:
            self.base_path: Path = Path(".")

        self.package = Package.parse_file(self.conf.resolve().as_posix())
        print(self.package.scripts)

    def initial_environment(self, arguments: list[str]) -> None:
        if len(arguments) > 0:
            print(f"initial_environment, Arguments: ({arguments})")
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")

        # config: configparser.ConfigParser = configparser.ConfigParser()
        # config.read(self.conf.resolve().as_posix())
        # # config["scripts"] = {"asd:asd": "asd"}
        # with open(self.conf.resolve().as_posix(), mode="w", encoding="utf-8") as configfile:
        #     config.write(configfile)

    def run_command(self, arguments: list[str]) -> None:
        # print(f"run_command, Arguments: ({arguments})")
        if len(arguments) != 1:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")
        if arguments[0] in self.package.scripts:
            BackendPackage._command_executor(commands=[self.package.scripts[arguments[0]]], shell=True)
        else:
            raise UnknownCommandError(f"Unknown command {arguments[0]} in [scripts]")
