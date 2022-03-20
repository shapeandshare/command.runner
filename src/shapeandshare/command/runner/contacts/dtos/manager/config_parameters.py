from ...backend_type import BackendType
from ..base_model import BaseModel


class ConfigParameters(BaseModel):
    type: BackendType
