"""Backend Type Definition"""

from enum import Enum


class BackendType(str, Enum):
    """Backend Type Enumeration"""

    CONFIG = "config"
    PACKAGE = "package"
