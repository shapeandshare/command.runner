""" Command Type Definition """

from enum import Enum


class CommandType(str, Enum):
    """Command Type Enumeration"""

    HELP = "help"
    INIT = "init"
    RUN = "run"
