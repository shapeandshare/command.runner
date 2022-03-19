from pydantic import BaseModel


class Package(BaseModel):
    scripts: dict
