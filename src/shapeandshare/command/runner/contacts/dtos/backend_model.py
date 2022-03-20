# pylint: disable=no-name-in-module
from pydantic import BaseModel


class BackendModel(BaseModel):
    scripts: dict
