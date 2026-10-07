import re
from typing import Any
from pydantic import BaseModel, model_validator
from src.config.logger import logger


class Required(BaseModel):
    """Reference model holding the default value of each required key.

    It is only used by ``GameConfig.validate_fields`` to know which keys
    are expected and which default replaces a missing or invalid value.

    Attributes:
        lives: Number of lives the player starts with.
        seed: Seed used to generate the first maze.
        super_gum_time: Seconds ghosts stay edible after a super-pacgum.
        level_max_time: Time limit of a level, in seconds.
        points_per_pacgum: Points earned for eating a pacgum.
        points_per_super_pacgum: Points earned for a super-pacgum.
        points_per_ghost: Points earned for eating an edible ghost.
        highscore_filename: Name of the json file storing highscores.
    """

    lives: int = 3
    seed: int = 42
    super_gum_time: int = 10
    level_max_time: int = 60
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 20
    points_per_ghost: int = 30
    highscore_filename: str = 'highscores.json'


class GameConfig(BaseModel):
    """Validated game configuration with default values.

    Attributes:
        width: Width of the maze.
        height: Height of the maze.
        lives: Number of lives the player starts with.
        seed: Seed used to generate the first maze.
        super_gum_time: Seconds ghosts stay edible after a super-pacgum.
        level_max_time: Time limit of a level, in seconds.
        points_per_pacgum: Points earned for eating a pacgum.
        points_per_super_pacgum: Points earned for a super-pacgum.
        points_per_ghost: Points earned for eating an edible ghost.
        highscore_filename: Name of the json file storing highscores.
    """

    width: int = 10
    height: int = 10
    lives: int = 3
    seed: int = 42
    super_gum_time: int = 10
    level_max_time: int = 60
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 20
    points_per_ghost: int = 30
    highscore_filename: str = "highscores.json"

    @model_validator(mode="before")
    @classmethod
    def validate_fields(cls, data: Any) -> dict:
        """Clean the raw configuration before pydantic validates it.

        Runs before the normal field validation. Unknown keys are
        reported, missing keys are reported, and invalid values (not a
        positive int, or not a valid json file name for the highscore
        file) are replaced by their default value. A warning is logged
        for each problem.

        Args:
            data: The raw data loaded from the configuration file, or
                None when no configuration is available.

        Returns:
            A dictionary with invalid values replaced by defaults. An
            empty dictionary is returned if ``data`` is None or is not
            a dictionary, so that every default is used.
        """
        if data is None:
            return {}
        if not isinstance(data, dict):
            logger.warning(
                "config file should be dict default config will be used"
            )
            return {}

        data_copy = data.copy()
        required_fields = Required.model_fields
        missing_keys = set(required_fields.keys()).difference(data.keys())
        for key, value in data.items():
            if key not in required_fields.keys():
                logger.warning(f"unknown key `{key}` will be ignored")
                continue

            default = required_fields[key].default
            if key != "highscore_filename" and (
                not isinstance(value, int) or value <= 0
            ):
                logger.warning(
                    f"`{key}` should be positive"
                    f" int will be replaced by {default}"
                )
                data_copy[key] = default
                continue
            if key == "highscore_filename":
                if not isinstance(value, str) or not re.search(
                    r"^\S+\.json$", value
                ):
                    logger.warning(
                        f"`{value}` should be valid json"
                        f" file will replaced by `{default}`"
                    )
                    data_copy[key] = default
        if missing_keys:
            logger.warning(f"missing keys: {missing_keys}")
        return data_copy
