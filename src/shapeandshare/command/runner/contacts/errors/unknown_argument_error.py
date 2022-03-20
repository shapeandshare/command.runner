"""Unknown Argument Error Definition"""


class UnknownArgumentError(Exception):
    """UnknownArgumentError"""

    command: str
    message: str

    # pylint: disable=super-init-not-called,fixme
    # TODO: address linting.
    def __init__(self, command: str, message: str):
        # super.__init__()
        self.command = command
        self.message = message

    def __str__(self):
        message: str = f"Command: {self.command}" + "\n" + self.message
        return message
