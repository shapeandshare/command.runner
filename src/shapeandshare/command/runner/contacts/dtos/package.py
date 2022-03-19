# pylint: disable=no-name-in-module
from pydantic import BaseModel


class Package(BaseModel):
    scripts: dict
