""" Backend Factory Definition"""

from typing import Optional, Union

from ..backends.backend_config import BackendConfig
from ..backends.backend_package import BackendPackage
from ..contacts.backend_type import BackendType


# pylint: disable=too-few-public-methods
class BackendFactory:
    """
    Backend Factory
    Factory class for the creation of backends.
    """

    @staticmethod
    def build(
        backend_type: BackendType, config_file: Optional[str] = None, base_path: Optional[str] = None
    ) -> Union[BackendConfig, BackendPackage]:
        """
        Our factory entry point
        Given the provided backend type and parameters will instantiate and return the result.

        Parameters
        ----------
        backend_type: The backend type to build.
        config_file: The configuration file to use when loading the backend.
        base_path: The location of the configuration file used when loading the backend.

        Returns
        -------
        The requested backend.
        """

        if backend_type == BackendType.CONFIG:
            return BackendConfig(config_file=config_file, base_path=base_path)
        return BackendPackage(config_file=config_file, base_path=base_path)
