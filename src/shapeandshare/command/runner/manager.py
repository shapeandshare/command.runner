import configparser
import json
import shlex
import subprocess
import sys
from enum import Enum
from pathlib import Path
from typing import Union

from .contacts.dtos.base_model import BaseModel
from .contacts.parse_error import ParseError
from .contacts.unknown_argument_error import UnknownArgumentError
from .contacts.unknown_command_error import UnknownCommandError


class CommandType(str, Enum):
    HELP = "help"
    INIT = "init"
    RUN = "run"


class Manager(BaseModel):
    base_file: str = "bcr.config"

    base_path: Path

    @property
    def conf(self) -> Path:
        return self.base_path / self.base_file

    def main(self) -> None:
        try:
            self.process()
        except UnknownCommandError as error:
            print(str(error))
            self.display_generic_help()
        except UnknownArgumentError as error:
            print(str(error))
        except ParseError as error:
            print(str(error))

    def process(self) -> None:
        argument_count: int = len(sys.argv)

        if argument_count == 1:
            self.display_generic_help()
        else:
            try:
                command: CommandType = CommandType(sys.argv[1])
                self.subcommand(subcommand=command, arguments=sys.argv[2:])
            except ValueError as error:
                raise UnknownCommandError(f"Unknown command {sys.argv[1]}") from error

    def subcommand(self, subcommand: CommandType, arguments=list[str]) -> None:
        if subcommand == CommandType.HELP:
            self.display_full_help()
        elif subcommand == CommandType.INIT:
            self.initial_environment(arguments=arguments)
        elif subcommand == CommandType.RUN:
            self.run_command(arguments=arguments)
        else:
            # should not be possible to hit
            raise UnknownCommandError(f"Unknown command {subcommand}")

    def display_generic_help(self) -> None:
        summary: str = "Usage: bcr <command>\n" "\n" "where <command> is one of:\n" "help, init, run"
        print(summary)

    def display_full_help(self):
        """TODO: Update!"""
        self.display_generic_help()

    def initial_environment(self, arguments: list[str]):
        if len(arguments) > 0:
            print(f"initial_environment, Arguments: ({arguments})")
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")

        config: configparser.ConfigParser = configparser.ConfigParser()
        config["scripts"] = {"hello": json.dumps(["echo hello world", "python -c 'print(\"hello world\")'"])}
        with open(self.conf.resolve().as_posix(), mode="w", encoding="utf-8") as configfile:
            config.write(configfile)

    def run_command(self, arguments: list[str]) -> None:
        print(f"run_command, Arguments: ({arguments})")
        if len(arguments) == 0:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")
        config: configparser.ConfigParser = configparser.ConfigParser()
        config.read(self.conf.resolve().as_posix())

        try:
            commands: Union[list, str] = json.loads(config["scripts"][arguments[0]])
        except KeyError as error:
            raise UnknownCommandError(f"Unknown command {arguments[0]} in [scripts]")
        except json.JSONDecodeError as error:
            raise ParseError(f"Unable to load [script] {arguments[0]}.  It was not JSON loadable.")

        # If given a single string then drop it into a list.
        if type(commands) == "str":
            commands = [commands]

        for command in commands:
            print(command)
            args = shlex.split(command)
            # output = Manager.shell_out(shell_out_cmd=command)
            with subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE) as process:
                print(process.stdout.read())
                print(process.stderr.read())
                # print(process.wait())
                # log.write(proc.stdout.read())
                # outs, errs = process.communicate(timeout=15)
            if process.returncode != 0:
                print(f"Failure while executing command: ({process.returncode})")

    # @staticmethod
    # def shell_out(shell_out_cmd: str) -> tuple[str, str, int]:
    #     args = shlex.split(shell_out_cmd)
    #     proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    #
    #     try:
    #         outs, errs = proc.communicate(timeout=60)
    #     except subprocess.TimeoutExpired:
    #         proc.kill()
    #         outs, errs = proc.communicate()
    #     return outs.decode(encoding="utf-8"), errs.decode(encoding="utf-8"), proc.returncode
