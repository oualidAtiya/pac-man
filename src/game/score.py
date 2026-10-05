import json
from pathlib import Path

from pydantic import BaseModel


class Score(BaseModel):
    name: str
    score: int


class IO:
    def __init__(self, path: Path = Path("highscores.json")):
        self.path = path

    def save(self, score: Score) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        highscores = [score.model_dump() for score in self.load()]
        highscores.append(score.model_dump())

        try:
            with open(self.path, "w") as f:
                json.dump(highscores, f, indent=2)
        except json.JSONDecodeError as e:
            print(f"ERROR: {e}")
        except PermissionError as e:
            print(f"ERROR: {e}")
        except FileNotFoundError as e:
            print(f"ERROR: {e}")

    def load(self) -> list[Score]:
        scores: list[Score] = []

        try:
            with open(self.path) as f:
                scores = [Score(**data) for data in json.load(f)]
        except json.JSONDecodeError as e:
            print(f"ERROR: {e}")
        except PermissionError as e:
            print(f"ERROR: {e}")
        except FileNotFoundError as e:
            print(f"ERROR: {e}")

        return sorted(scores, key=lambda score: score.score, reverse=True)
