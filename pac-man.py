from src.config.loader import Loader
from src.game.ghost import Ghost, GhostColor
from src.game.player import Player
from src.game.state import GameState
from src.maze.maze import Maze
from src.ui.render import Renderer
from src.game.pacgum import Pacgum

def main():
    loader = Loader()
    config = loader.load_config()
    if config:
        maze = Maze(config)
        state = GameState(
            maze=maze,
            player=Player(maze),
            ghosts=[
                Ghost((0, 0), GhostColor.RED),
                Ghost((maze.width - 1, 0), GhostColor.BLUE),
                Ghost((0, maze.height - 1), GhostColor.PINK),
                Ghost((maze.width - 1, maze.height - 1), GhostColor.ORANGE),
            ],
            pacgum=Pacgum(maze)
        )
        render = Renderer(2000, 1500)
        render.run(state)


if __name__ == "__main__":
    main()
