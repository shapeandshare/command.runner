from typing import Union

from ..backends.backend_config import BackendConfig
from ..backends.backend_package import BackendPackage
from ..contacts.backend_type import BackendType


class BackendFactory:
    @staticmethod
    def build(backend_type: BackendType) -> Union[BackendConfig, BackendPackage]:
        if backend_type == BackendType.CONFIG:
            return BackendConfig()
        return BackendPackage()
