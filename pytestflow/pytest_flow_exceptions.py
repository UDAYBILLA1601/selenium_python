class PyTestFlowException(Exception):
    """
    Custom exception class to represent errors specific to test flow processes.

    Attributes:
    - message (str): A description of the error encountered.

    Methods:
    - __init__(message): Initializes the exception with a provided error message.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)