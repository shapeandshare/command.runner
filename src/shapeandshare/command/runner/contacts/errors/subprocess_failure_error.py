"""Subprocess Failure Error Definition"""
import json


class SubprocessFailureError(Exception):
    """Subprocess Failure Error"""

    command: str
    message: str
    returncode: int

    # pylint: disable=super-init-not-called,fixme
    # TODO: address linting.
    def __init__(self, command: str, message: str, returncode: int):
        # super.__init__()
        self.command = command
        self.message = message
        self.returncode = returncode

    def __str__(self):
        message: str = json.dumps({"command": self.command, "message": self.message, "returncode": self.returncode})
        return message
