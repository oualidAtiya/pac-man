import json
import re
from argparse import ArgumentParser, ArgumentTypeError
from typing import Any

from src.config.logger import logger
from src.config.models import GameConfig


class Loader:
    """Load and validate the game configuration from a JSON file.

    The file name is read from the command line. The file may contain
    comments, which are removed before parsing. Any problem with the
    file is logged and the default configuration is used instead.

    Attributes:
        file_name: Path of the configuration file given by the user.
    """

    def __init__(self) -> None:
        """Initialize the loader by parsing the command line arguments."""
        self.file_name = Loader.parse_file_name()

    @staticmethod
    def json_type(value: str) -> str:
        """Check that a command line value looks like a json file name.

        Used as the ``type`` callback of argparse.

        Args:
            value: The raw command line argument.

        Returns:
            The same value if it ends with ``.json`` and has no spaces.

        Raises:
            ArgumentTypeError: If the value is not a valid json file name.
        """
        pattern = r"^\S+\.json$"
        if not re.search(pattern, value):
            raise ArgumentTypeError(
                f"\033[1;96minvalid json type value: '{value}'"
            )
        return value

    @staticmethod
    def parse_file_name() -> str:
        """Parse the command line and get the configuration file name.

        Returns:
            The name of the json configuration file.
        """
        parser = ArgumentParser()
        parser.add_argument("file_name", type=Loader.json_type)
        args = parser.parse_args()
        return str(args.file_name)

    def read_config_file(self) -> list[str]:
        """Read the configuration file line by line.

        Returns:
            The lines of the file, including their newline characters.

        Raises:
            FileNotFoundError: If the file does not exist.
            PermissionError: If the file cannot be read.
            IsADirectoryError: If the path points to a directory.
        """
        with open(self.file_name) as config:
            return config.readlines()

    @staticmethod
    def strip_comments(content: list[str]) -> str:
        """Remove comments from the configuration content.

        Lines starting with ``#`` are dropped, and anything after a
        ``#`` on other lines is ignored.

        Args:
            content: The lines of the configuration file.

        Returns:
            The content without comments, joined into a single string.
        """
        striped_content: list[str] = []
        for line in content:
            if not re.search(r"^\s*#", line):
                striped_content += line.split("#")[0]
        return "".join(striped_content)

    @staticmethod
    def check_duplicate(pairs: list[tuple[Any, Any]]) -> dict:
        """Build a dictionary from json pairs and warn about duplicates.

        Used as the ``object_pairs_hook`` of ``json.loads``. When a key
        appears more than once, a warning is logged and the last value
        is kept.

        Args:
            pairs: The (key, value) pairs of a json object, in order.

        Returns:
            A dictionary built from the pairs.
        """
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
        """Load, parse and validate the configuration file.

        If the file is missing, unreadable, a directory, empty or not
        valid json, a message is logged and the default configuration
        is returned instead of raising an error.

        Returns:
            The validated game configuration.
        """
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
            logger.warning(f"{self.file_name} should be file not a directory")
            return GameConfig.model_validate(None)

        striped_content = Loader.strip_comments(content)
        if not striped_content:
            logger.warning("file is empty default config will be used")
            return GameConfig.model_validate(None)
        try:
            data = json.loads(
                striped_content, object_pairs_hook=Loader.check_duplicate
            )
        except json.JSONDecodeError as err:
            error_line = err.doc.split("\n")[err.lineno - 1]
            logger.json_error(error_line, self.file_name)
            return GameConfig.model_validate(None)

        config = GameConfig.model_validate(data)
        return config
