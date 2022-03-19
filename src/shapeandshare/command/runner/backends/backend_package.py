from pathlib import Path
from typing import Optional

from ..contacts.errors.unknown_argument_error import UnknownArgumentError


class BackendPackage:
    config_file: str
    base_path: Path

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = "bcr.config"
        if base_path:
            self.base_path: Path = Path(base_path)
        else:
            self.base_path: Path = Path(".")

    @property
    def conf(self) -> Path:
        return self.base_path / self.config_file

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
        if len(arguments) == 0:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")
