from src.config.loader import Loader
from src.game.ghost import Ghost
from src.game.player import Player
from src.game.state import GameState
from src.maze.maze import Maze
from src.ui.render import Renderer


def main():
    loader = Loader()
    config = loader.load_config()
    if config:
        maze = Maze(config)
        state = GameState(
            maze=maze,
            player=Player((0, 0), config.lives),
            ghosts=[
                Ghost((0, 0), "red"),
                Ghost((0, 0), "blue"),
                Ghost((0, 0), "green"),
                Ghost((0, 0), "yellow"),
            ],
        )
        render = Renderer(2000, 1500)
        render.run(state)


if __name__ == "__main__":
    main()
