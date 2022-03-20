""" Backend Abstract Definition """

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..contacts.dtos.backend_model import BackendModel
from ..contacts.errors.subprocess_failure_error import SubprocessFailureError
from ..contacts.errors.unknown_argument_error import UnknownArgumentError
from ..contacts.errors.unknown_command_error import UnknownCommandError


class AbstractBackend(ABC):
    """
    Abstract Backend DTO

    Attributes
    ----------
    config_file
        The file specific to the backend being used.
    base_path
        The path to the config file.
    DEFAULT_CONFIG_FILE
        The default config file, defined within each super-class.
    DEFAULT_CONFIG_PATH
        The default location for the configuration file, default: Path(".")
    model
        BackendModel DTO
    """

    config_file: str
    base_path: Path
    DEFAULT_CONFIG_FILE: str
    DEFAULT_CONFIG_PATH: Path = Path(".")
    model: BackendModel

    def __init__(self, config_file: Optional[str] = None, base_path: Optional[str] = None):
        if config_file:
            self.config_file = config_file
        else:
            self.config_file = self.DEFAULT_CONFIG_FILE
        if base_path:
            self.base_path: Path = Path(base_path)
        else:
            self.base_path: Path = self.DEFAULT_CONFIG_PATH

    @property
    def conf(self) -> Path:
        """
        Class Property
        Path to backend specific config file.

        Returns
        -------
        Full path of configuration file.
        """

        return self.base_path / self.config_file

    @abstractmethod
    def init_environment(self, arguments: list[str]) -> None:
        """
        Initialize Environment

        Parameters
        ----------
        arguments: The arguments to used to build the default configuration.
        """

    @staticmethod
    def _command_executor(commands: list[str], per_command_timeout: Optional[int] = None) -> None:
        """
        Handles command execution.

        Parameters
        ----------
        commands: The list of commands to execute.
        per_command_timeout: The per-command timeout threshold.
        """

        # Command executor
        for command in commands:
            print(", ".join([thing for thing in command]))
            with subprocess.Popen(command, shell=True) as process:
                try:
                    process.wait(timeout=per_command_timeout)
                except subprocess.TimeoutExpired as error:
                    raise SubprocessFailureError(
                        f"command {command} exceeded timeout limit of {per_command_timeout}"
                    ) from error

    def run_command(self, arguments: list[str], per_command_timeout: Optional[int] = None) -> None:
        """
        Run a command

        Parameters
        ----------
        arguments: The arguments to execute.
        per_command_timeout: The per-command time out threshold.
        """

        if len(arguments) != 1:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")
        if arguments[0] in self.model.scripts:
            AbstractBackend._command_executor(
                commands=[self.model.scripts[arguments[0]]], per_command_timeout=per_command_timeout
            )
        else:
            raise UnknownCommandError(f"Unknown command {arguments[0]} in [scripts]")
