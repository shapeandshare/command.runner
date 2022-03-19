from enum import Enum


class CommandType(str, Enum):
    HELP = "help"
    INIT = "init"
    RUN = "run"
