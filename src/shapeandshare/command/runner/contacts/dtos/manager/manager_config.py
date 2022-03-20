""" Manager Configuration Definition"""

from ..base_model import BaseModel
from .command_parameters import CommandParameters
from .config_parameters import ConfigParameters


class ManagerConfig(BaseModel):
    """
    ManagerConfig dto

    Attributes
    ----------
    command: Manager Command Parameters DTO
    config: Manager Config Parameters DTO
    """

    command: CommandParameters
    config: ConfigParameters
