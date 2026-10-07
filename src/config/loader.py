from argparse import ArgumentParser, ArgumentTypeError
import re
from typing import Any
from src.config.models import GameConfig
from src.config.logger import logger
import json


class Loader:

    def __init__(self) -> None:
        self.file_name = Loader.parse_file_name()

    @staticmethod
    def json_type(value: str) -> str:
        pattern = r"^\S+\.json$"
        if not re.search(pattern, value):
            raise ArgumentTypeError(
                f"\033[1;96minvalid json type value: '{value}'"
            )
        return value

    @staticmethod
    def parse_file_name() -> str:
        parser = ArgumentParser()
        parser.add_argument('file_name', type=Loader.json_type)
        args = parser.parse_args()
        return args.file_name

    def read_config_file(self) -> list[str]:
        with open(self.file_name) as config:
            return config.readlines()

    @staticmethod
    def strip_comments(content: list[str]) -> str:
        striped_content: list[str] = []
        for line in content:
            if not re.search(r"^\s*#", line):
                striped_content += line.split('#')[0]
        return "".join(striped_content)

    @staticmethod
    def check_duplicate(pairs: list[tuple[Any, Any]]) -> dict:
        seen = set()
        duplicated = []
        for key, _ in pairs:
            if key in seen:
                duplicated.append(key)
                continue
            seen.add(key)
        if duplicated:
            logger.warning(f"duplicated keys: {duplicated}")
        return dict(pairs)

    def load_config(self) -> GameConfig:
        try:
            content = self.read_config_file()
        except PermissionError:
            logger.warning(
                f"'{self.file_name}' file don't have"
                "permission default config will be used"
            )
            return GameConfig.model_validate(None)
        except FileNotFoundError:
            logger.warning(
                f"'{self.file_name}' file not "
                "found default config will be used"
            )
            return GameConfig.model_validate(None)
        except IsADirectoryError:
            logger.warning(f"{self.path} should be file not a directory")
            return GameConfig.model_validate(None)

        striped_content = Loader.strip_comments(content)
        if not striped_content:
            logger.warning("file is empty default config will be used")
            return GameConfig.model_validate(None)
        try:
            data = json.loads(
                striped_content,
                object_pairs_hook=Loader.check_duplicate
            )
        except json.JSONDecodeError as err:
            error_line = err.doc.split('\n')[err.lineno-1]
            logger.json_error(error_line, self.file_name)
            return GameConfig.model_validate(None)

        config = GameConfig.model_validate(data)
        return config
