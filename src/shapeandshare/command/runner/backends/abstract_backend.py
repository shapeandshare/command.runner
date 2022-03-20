import subprocess
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

from ..contacts.errors.subprocess_failure_error import SubprocessFailureError


class AbstractBackend(ABC):
    config_file: str
    base_path: Path

    @property
    def conf(self) -> Path:
        return self.base_path / self.config_file

    @abstractmethod
    def initial_environment(self, arguments: list[str]) -> None:
        """initial_environment"""

    @abstractmethod
    def run_command(self, arguments: list[str], per_command_timeout: Optional[int] = None) -> None:
        """run_command"""

    @staticmethod
    def _command_executor(commands: list[str], per_command_timeout: Optional[int] = None) -> None:
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
