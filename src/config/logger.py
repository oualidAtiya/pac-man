class Logger:
    """Print colored warning and error messages to the terminal.

    Attributes:
        warning_id: Number of warnings printed so far, used to number
            each new warning.
    """

    def __init__(self) -> None:
        """Initialize the logger with the warning counter set to zero."""
        self.warning_id = 0

    def warning(self, msg: str) -> None:
        """Print a numbered warning message in yellow.

        Args:
            msg: The warning text to display.
        """
        self.warning_id += 1
        print(f"\033[1;33mWarning #{self.warning_id}: {msg}\033[0m")

    def error(self, msg: str) -> None:
        """Print an error message in red.

        Args:
            msg: The error text to display.
        """
        print(f"\033[1;31mError : {msg}\033[0m")

    def json_error(self, error_line: str, file_name: str) -> None:
        """Print a json syntax error with the faulty line highlighted.

        Args:
            error_line: The line of the file where parsing failed.
            file_name: The name of the file that contains the error.
        """
        print(
            f"\033[91;1mJson Error ({file_name}): "
            ">>>\033[0m{error_line}\033[91;1m<<<\033[0m"
        )

    def pydantic_error(self, errs: dict) -> None:
        """Print the validation errors reported by pydantic.

        For each error, the name of the faulty key is printed when the
        error location is deep enough, followed by the error message.

        Args:
            errs: The validation errors, as returned by pydantic.
        """
        for err in errs:
            if (len(err.get('loc')) > 2):
                key = err.get("loc")
                print(
                    f"\033[1;91mPydnatic Error ({key[2]}):\033[0m", end="")
            if (err.get('msg', False)):
                print(f"\033[1;91m {err.get('msg')}\033[0m")


logger = Logger()
