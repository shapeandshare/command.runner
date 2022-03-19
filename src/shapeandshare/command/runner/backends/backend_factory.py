from typing import Union

from ..backends.backend_package import BackendPackage
from ..contacts.backend_type import BackendType
from ..backends.backend_config import BackendConfig
from ..contacts.errors.unknown_backend_error import UnknownBackendError


class BackendFactory:
    @staticmethod
    def build(backend_type: BackendType) -> Union[BackendConfig, BackendPackage]:
        if backend_type == BackendType.CONFIG:
            return BackendConfig()
        elif backend_type == BackendType.PACKAGE:
            return BackendPackage()

        message: str = f"Backend {backend_type} requested, but only {BackendType.CONFIG} and {BackendType.PACKAGE} are currently supported"
        raise UnknownBackendError(message)
