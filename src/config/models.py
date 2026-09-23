from pydantic import BaseModel, Field, StringConstraints, ConfigDict
from typing import Annotated

type_int = Annotated[int, Field(gt=0)]


class Level(BaseModel):
    width: type_int
    height: type_int

    model_config = ConfigDict(extra='forbid', strict=True)
    

class GameConfig(BaseModel):
    lives: type_int
    seed: type_int
    level_max_time: type_int
    points_per_pacgum: type_int
    points_per_super_pacgum: type_int
    points_per_ghost: type_int
    highscore_filename: Annotated[str, StringConstraints(pattern=r"\S+\.json")]
    levels: Annotated[list[Level], Field(min_length=1)]

    model_config = ConfigDict(extra='forbid', strict=True)

class Data(BaseModel):
    data: GameConfig