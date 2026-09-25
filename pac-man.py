from src.config.loader import Loader
from src.maze.maze import Maze
import pygame



def main():
    loader = Loader()
    config = loader.load_config()
    if not config:
        return

    pygame.init()
    maze = Maze(config)
    screen = pygame.display.set_mode((2000, 1500))
    clock = pygame.time.Clock()
    
    is_run = True
    while is_run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_run = False
        screen.fill((0, 0, 0))
        maze.draw(screen, 520, 170)
        pygame.display.flip()
        clock.tick(60)
    
if __name__ == '__main__':
    main()
