from enum import Enum


class BackendType(str, Enum):
    CONFIG = "config"
    PACKAGE = "package"
