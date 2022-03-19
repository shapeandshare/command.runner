import shlex
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

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
    def run_command(self, arguments: list[str]) -> None:
        """run_command"""

    @staticmethod
    def _command_executor(commands: list[str]) -> None:
        # Command executor

        for command in commands:
            print(command)
            args = shlex.split(command)
            with subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                while True:
                    output_stdout = process.stdout.readline()
                    output_stderr = process.stderr.readline()
                    if output_stdout:
                        print(output_stdout.decode(encoding="utf-8").strip())
                    if output_stderr:
                        print(output_stderr.decode(encoding="utf-8").strip())
                    if process.poll() is not None:
                        break

                return_code: int = process.poll()
            if return_code != 0:
                raise SubprocessFailureError(f"{command} failed with exit code {return_code}")
