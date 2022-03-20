""" Backend Abstract Definition """

import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..contacts.errors.subprocess_failure_error import SubprocessFailureError


class AbstractBackend(ABC):
    """
    Abstract Backend DTO

    Attributes
    ----------
    config_file
        The file specific to the backend being used.
    base_path
        The path to the config file.
    """

    config_file: str
    base_path: Path

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

    @abstractmethod
    def run_command(self, arguments: list[str], per_command_timeout: Optional[int] = None) -> None:
        """
        Run a command

        Parameters
        ----------
        arguments: The arguments to execute.
        per_command_timeout: The per-command time out threshold.
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
            print(command)
            with subprocess.Popen(command, shell=True) as process:
                try:
                    process.wait(timeout=per_command_timeout)
                except subprocess.TimeoutExpired as error:
                    raise SubprocessFailureError(
                        f"command {command} exceeded timeout limit of {per_command_timeout}"
                    ) from error
