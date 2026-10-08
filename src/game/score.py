import json
from pathlib import Path
from src.config.logger import logger
from pydantic import BaseModel, ValidationError, Field, ConfigDict


class Score(BaseModel):
    """A single highscore entry.

    Attributes:
        name: The player name, 1 to 10 letters, digits or spaces.
        score: The points obtained, validated as a positive integer.
    """

    name: str = Field(pattern=r"^[A-Za-z0-9 ]+$", max_length=10)
    score: int = Field(gt=0, lt=9999999999)

    model_config = ConfigDict(extra='forbid')


class Data(BaseModel):
    """The content of a highscore file, used for validation.

    Attributes:
        scores: The list of highscore entries stored in the file.
    """

    scores: list[Score]


class IO:
    """Read and write the highscores in a json file.

    Every file problem is logged as a warning instead of raising an
    error, so a bad file never crashes the game.

    Attributes:
        path: The path of the highscore file.
    """

    def __init__(self, path: str) -> None:
        """Create the highscore reader and writer.

        Args:
            path: The path of the highscore json file.
        """
        self.path = Path(path)

    def save(self, score: Score) -> None:
        """Add a score to the highscore file.

        The existing scores are loaded, the new one is appended, and
        the whole list is written back as json. The parent folder is
        created if needed. Write errors are logged, not raised.

        Args:
            score: The new score to store.
        """
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
            logger.warning("unxpected error happend")

    def load(self) -> list[Score]:
        """Read and validate the scores from the highscore file.

        The file must contain a non-empty json list of valid scores.
        If anything is wrong (missing file, bad json, invalid entry,
        permission problem), the problem is logged and an empty list
        is returned.

        Returns:
            The scores sorted from highest to lowest, or an empty list
            if the file could not be read or validated.
        """
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
                scores = Data(scores=data).scores
                is_error = False
        except ValidationError as e:
            logger.pydantic_error(json.loads(e.json()))
        except json.JSONDecodeError as err:
            error_line = err.doc.split('\n')[err.lineno-1]
            logger.json_error(error_line, self.path.name)
        except PermissionError:
            logger.warning(f"{self.path.name} don't have read permission")
        except FileNotFoundError:
            logger.warning(f"{self.path.name} not found")
        except IsADirectoryError:
            logger.warning(f"{self.path.name} should be file not a directory")
        except ValueError as e:
            logger.json_error(str(e), self.path.name)
        except Exception:
            logger.warning("unxpected error happend")
        if not is_error:
            return sorted(scores, key=lambda score: score.score, reverse=True)
        return []
