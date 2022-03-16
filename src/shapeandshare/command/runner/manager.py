import sys
from enum import Enum

from .contacts.dtos.base_model import BaseModel
from .contacts.unknown_subcommand_error import UnknownCommandError


class SubCommandType(str, Enum):
    help = "help"
    init = "init"
    run = "run"


class Manager(BaseModel):
    def main(self):
        try:
            self.process()
        except UnknownCommandError as error:
            self.display_generic_help()

    def process(self):
        argument_count: int = len(sys.argv)

        if argument_count == 1:
            self.display_generic_help()
        else:
            try:
                subcommand: SubCommandType = SubCommandType(sys.argv[1])
                print(f"Command: {subcommand}")
                self.subcommand(subcommand=subcommand, arguments=sys.argv[2:])
            except ValueError as error:
                raise UnknownCommandError(f"Unknown command {sys.argv[1]}") from error

    def display_generic_help(self):
        summary: str = "Usage: bcr <command>\n" "\n" "where <command> is one of:\n" "help, init, run"
        print(summary)

    def subcommand(self, subcommand: SubCommandType, arguments=list[str]):
        print(f"Subcommand: ({subcommand}), arguments: ({arguments})")
