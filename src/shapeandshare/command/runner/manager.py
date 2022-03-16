import sys
from enum import Enum

from .contacts.dtos.base_model import BaseModel
from .contacts.unknown_argument_error import UnknownArgumentError
from .contacts.unknown_command_error import UnknownCommandError


class CommandType(str, Enum):
    help = "help"
    init = "init"
    run = "run"


class Manager(BaseModel):
    def main(self) -> None:
        try:
            self.process()
        except UnknownCommandError as error:
            self.display_generic_help()
        except UnknownArgumentError as error:
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

    def display_generic_help(self) -> None:
        summary: str = "Usage: bcr <command>\n" "\n" "where <command> is one of:\n" "help, init, run"
        print(summary)

    def display_full_help(self):
        """TODO: Update!"""
        self.display_generic_help()

    def initial_environment(self, arguments: list[str]):
        print(f"initial_environment, Arguments: ({arguments})")
        if len(arguments) > 0:
            raise UnknownArgumentError(command="init", message="No arguments to init are supported!")

    def run_command(self, arguments: list[str]):
        print(f"run_command, Arguments: ({arguments})")
        if len(arguments) != 1:
            raise UnknownArgumentError(command="run", message="Expected exactly 1 argument to run!")

    def subcommand(self, subcommand: CommandType, arguments=list[str]) -> None:
        if subcommand == CommandType.help:
            self.display_full_help()
        elif subcommand == CommandType.init:
            self.initial_environment(arguments=arguments)
        elif subcommand == CommandType.run:
            self.run_command(arguments=arguments)
        else:
            # should not be possible to hit
            raise UnknownCommandError(f"Unknown command {subcommand}")
