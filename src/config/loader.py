from argparse import ArgumentParser, ArgumentTypeError
import re
from pydantic import ValidationError
from src.config.models import Data, GameConfig
import json

class Loader:

    def __init__(self):
        self.file_name = Loader.parse_file_name()

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
        try:
            with open(self.file_name) as config:
                return config.readlines()
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

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
                index = keys[1]
                key = ".".join([str(key) for key in keys[2:]])
                print(
                    f"\033[1;91mError #{i} at field `data[{index}].{key}`:\033[0m")
            if (err.get('msg', False)):
                print(f"\033[1;96mMessage: {err.get('msg')}\033[0m")
            if (err.get('type', False)):
                print(f"\033[1;92mError Type: {err.get('type')}\033[0m")

    def load_config(self) -> GameConfig | None:
        content = self.read_config_file()
        striped_content = Loader.strip_comments(content)
        try:
            data = json.loads(striped_content)
        except json.JSONDecodeError as err:
            error_line = err.doc.split('\n')[err.lineno-1]
            msg = (
                f"\033[92m Error: >>>\033[0m{error_line}\033[92m<<<\033[0m"
            )
            print(msg)
            return

        config_error = False
        try:
            config = Data(data=data).data
        except ValidationError as errs:
            Loader.format_errors(json.loads(errs.json()))
            config_error = True
        if config_error:
            default = {
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
            config = GameConfig(**default)
        return config