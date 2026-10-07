class Logger:
    def __init__(self):
        self.warning_id = 0

    def warning(self, msg: str) -> None:
        self.warning_id += 1
        print(f"\033[1;33mWarning #{self.warning_id}: {msg}\033[0m")

    def error(self, msg: str) -> None:
        print(f"\033[1;31mError : {msg}\033[0m")

    def json_error(self, error_line: str, file_name: str) -> None:
        print(
            f"\033[91;1mJson Error: >>>\033[0m{error_line}\033[91;1m<<<\033[0m"
        )

    def pydantic_error(self, errs: dict) -> None:
        for err in errs:
            if (len(err.get('loc')) > 2):
                key = err.get("loc")
                print(
                    f"\033[1;91mPydnatic Error ({key[2]}):\033[0m", end="")
            if (err.get('msg', False)):
                print(f"\033[1;91m {err.get('msg')}\033[0m")

logger = Logger()
