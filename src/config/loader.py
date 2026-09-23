from argparse import ArgumentParser, ArgumentTypeError
import re
from pydantic import ValidationError
from src.config.models import Data, GameConfig
import json

class Loader:

    def __init__(self) -> None:
        self.file_name = Loader.parse_file_name()
        self.config = {
            "lives": 3,
            "seed": 42,
            "level_max_time": 90,
            "points_per_pacgum": 10,
            "points_per_super_pacgum": 50,
            "points_per_ghost": 200,
            "highscore_filename": "highscores.json",
            "levels": [
                {"width": 10, "height": 21},
                {"width": 25, "height": 25},
                {"width": 31, "height": 31}
            ]
        }

    @staticmethod
    def json_type(value: str) -> str:
        pattern = r"^\S+\.json$"
        if not re.search(pattern, value):
            raise ArgumentTypeError(f"\033[1;96minvalid json type value: '{value}'")
        return value

    @staticmethod
    def parse_file_name() -> str:
        parser = ArgumentParser()
        parser.add_argument('file_name', type=Loader.json_type)
        args = parser.parse_args()
        return args.file_name

    def read_config_file(self) -> list[int]:
        with open(self.file_name) as config:
            return config.readlines()

    @staticmethod
    def strip_comments(content: list[str]) -> str:
        striped_content = []
        for line in content:
            if not re.search(r"^\s*#", line):
                striped_content += line.split('#')[0]
        return "".join(striped_content)

    @staticmethod
    def format_errors(errs: dict) -> None:
        for i, err in enumerate(errs, 1):
            if (len(err.get('loc')) > 1):
                keys = err.get("loc")
                if (len(keys) == 2):
                    key = err.get("loc")[-1]
                elif (len(keys) == 4):
                    key = ".".join([keys[1], keys[-1]])

                print(f"\033[1;33mWarning #{i} at field ({key}):\033[0m", end=" ")
            if (err.get('msg', False)):
                print(f"\033[1;32m{err.get('msg')}\033[0m")

    def load_config(self) -> GameConfig | None:
        config_error = False
        try:
            content = self.read_config_file()
        except PermissionError:
            print(f"\033[1;31m'{self.file_name}': File Don't Have Permission:\033[0m")
            return
        except FileNotFoundError:
            print(f"\033[1;31m'{self.file_name}': File Not Found\033[0m")
            return

        striped_content = Loader.strip_comments(content)
        try:
            data = json.loads(striped_content)
        except json.JSONDecodeError as err:
            error_line = err.doc.split('\n')[err.lineno-1]
            msg = (
                f"\033[91;1mJson Error: >>>\033[0m{error_line}\033[91;1m<<<\033[0m"
            )
            print(msg)
            return

        try:
            config = Data(data=data).data
        except ValidationError as errs:
            Loader.format_errors(json.loads(errs.json()))
            config_error = True
        if config_error:
            config = GameConfig(**self.config)
        return config