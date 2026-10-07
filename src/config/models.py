import re
from typing import Any
from pydantic import BaseModel, model_validator
from src.config.logger import logger


class Required(BaseModel):
    lives: int = 3
    seed: int = 42
    super_gum_time: int = 10
    level_max_time: int = 60
    points_per_pacgum: int = 10
    points_per_super_pacgum: int = 20
    points_per_ghost: int = 30
    highscore_filename: str = 'highscores.json'


class GameConfig(BaseModel):
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
