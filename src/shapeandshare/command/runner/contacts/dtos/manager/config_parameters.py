""" Manager Config Config Parameters """

from typing import Optional

from ...backend_type import BackendType
from ..base_model import BaseModel


# pylint: disable=too-few-public-methods
class ConfigParameters(BaseModel):
    """
    ConfigParameters DTO

    Attributes
    ----------
    type: The backendtype
    file: The backend configuration filename.
    path: The path to the backend configuration file.
    """

    type: BackendType
    file: Optional[str]
    path: Optional[str]
