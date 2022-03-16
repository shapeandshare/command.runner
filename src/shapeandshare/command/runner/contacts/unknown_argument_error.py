class UnknownArgumentError(Exception):
    """UnknownArgumentError"""

    command: str
    message: str

    def __init__(self, command: str, message: str):
        self.command = command
        self.message = message

    def __str__(self):
        message: str = f"Command: {self.command}" + "\n" + self.message
        return message
