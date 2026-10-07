class Logger:
    def __init__(self):
        self.warning_id = 0

    def warning(self, msg: str) -> None:
        self.warning_id += 1
        print(f"\033[1;33mWarning #{self.warning_id}: {msg}\033[0m")

    def json_error(self, error_line: str) -> None:
        print(
            f"\033[91;1mJson Error: >>>\033[0m{error_line}\033[91;1m<<<\033[0m"
        )


logger = Logger()
