from typing import Optional

from ...backend_type import BackendType
from ..base_model import BaseModel


class ConfigParameters(BaseModel):
    type: BackendType
    file: Optional[str]
    path: Optional[str]
