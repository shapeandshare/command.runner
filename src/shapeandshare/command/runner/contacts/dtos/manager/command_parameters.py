""" Manager Config Command Parameters"""
from typing import Optional

from ..base_model import BaseModel


class CommandParameters(BaseModel):
    """
    CommandParameters DTO

    Attributes
    ----------
    timeout: The maximum duration (in seconds) a process can run before being stopped.
    """

    timeout: Optional[int]
