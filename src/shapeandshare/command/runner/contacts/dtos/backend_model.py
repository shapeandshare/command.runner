""" Backend Model (Data Storage)"""

# pylint: disable=no-name-in-module,too-few-public-methods
from pydantic import BaseModel


class BackendModel(BaseModel):
    """
    BackendModel DTO

    Attributes
    ----------
    scripts: The alias : command map
    """

    scripts: dict
