from src.config.loader import Loader
from src.maze.maze import Maze
def main():
    loader = Loader()
    config = loader.load_config()
    if config:
        maze = Maze(config)
        for row in maze.grid:
            print(row)
    
if __name__ == '__main__':
    main()
