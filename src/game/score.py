import json
from pathlib import Path
from src.config.logger import logger
from pydantic import BaseModel, ValidationError, Field, ConfigDict
import json

class Score(BaseModel):
    name: str = Field(pattern=r"^[A-Za-z0-9]+$")
    score: int = Field(gt=0, lt=9999999999)

    model_config = ConfigDict(extra='forbid')

class Data(BaseModel):
    scores : list[Score]

class IO:
    def __init__(self, path: str) -> None:
        self.path = Path(path)

    def save(self, score: Score) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        highscores = [score.model_dump() for score in self.load()]
        highscores.append(score.model_dump())

        try:
            with open(self.path, "w") as f:
                json.dump(highscores, f, indent=2)
        except PermissionError:
            logger.warning(f"{self.path} don't have write permission")
        except IsADirectoryError:
            logger.warning(f"{self.path} should be file not a directory")
        except Exception:
            logger.warning(f"unxpected error happend")

    def load(self) -> list[Score] | list[None]:
        scores: list[Score] = []
        is_error = True
        try:
            with open(self.path) as f:
                data = f.read()
                if not data.strip():
                    raise ValueError("file cannot be empty")
                data = json.loads(data)
                if not isinstance(data, list):
                    raise ValueError("data should be wrapped in list")
                scores = Data(scores=data)
                is_error = False
        except ValidationError as e:
            logger.pydantic_error(json.loads(e.json()))
        except json.JSONDecodeError as err:
            error_line = err.doc.split('\n')[err.lineno-1]
            logger.json_error(error_line, self.path)
        except PermissionError:
            logger.warning(f"{self.path} don't have read permission")
        except FileNotFoundError:
            logger.warning(f"{self.path} not found")
        except IsADirectoryError:
            logger.warning(f"{self.path} should be file not a directory")
        except ValueError as e:
            logger.json_error(e, self.path)
        except Exception:
            logger.warning(f"unxpected error happend")
        if not is_error:
            return sorted(scores.scores, key=lambda score: score.score, reverse=True)
        return []
