from src.config.loader import Loader
from src.game.ghost import Ghost, GhostColor
from src.game.player import Player
from src.game.state import GameState
from src.maze.maze import Maze
from src.ui.render import Renderer
from src.game.pacgum import Pacgum
from src.maze.generator_error import GeneratorError
from src.config.logger import logger

def main() -> None:
    loader = Loader()
    config = loader.load_config()
    maze = Maze(config)
    state = GameState(
        maze=maze,
        player=Player(maze),
        ghosts=[
            Ghost((0, 0), GhostColor.RED),
            Ghost((maze.config.width - 1, 0), GhostColor.BLUE),
            Ghost((0, maze.config.height - 1), GhostColor.PINK),
            Ghost((maze.config.width - 1, maze.config.height - 1), GhostColor.ORANGE),
        ],
        pacgum=Pacgum(maze)
    )
    render = Renderer(2000, 1500)
    render.run(state)


if __name__ == "__main__":
    try:
        main()
    except GeneratorError as e:
        logger.error(e)
    except Exception as e:
        logger.error(e)
