""" Backend Model (Data Storage)"""

# pylint: disable=no-name-in-module
from pydantic import BaseModel


class BackendModel(BaseModel):
    """
    BackendModel DTO

    Attributes
    ----------
    scripts: The alias : command map
    """

    scripts: dict
