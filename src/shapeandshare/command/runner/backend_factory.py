from .contacts.backend_type import BackendType
from .contacts.dtos.config_backend import ConfigBackend
from .contacts.errors.unknown_backend_error import UnknownBackendError


class BackendFactory:
    @staticmethod
    def build(backend_type: BackendType) -> ConfigBackend:
        if backend_type == BackendType.CONFIG:
            return ConfigBackend()
        # elif backend_type == BackendType.PACKAGE:
        #
        # else:
        message: str = f"Backend {backend_type} requested, but only {BackendType.CONFIG} is currently supported"
        raise UnknownBackendError(message)
