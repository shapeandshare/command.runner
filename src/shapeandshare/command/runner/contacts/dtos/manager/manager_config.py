from ..base_model import BaseModel
from .command_parameters import CommandParameters
from .config_parameters import ConfigParameters


class ManagerConfig(BaseModel):
    command: CommandParameters
    config: ConfigParameters
