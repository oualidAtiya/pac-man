
class GeneratorError(Exception):
    """Error raised when the maze generation fails.

    It is raised by ``Maze`` when the assigned A-Maze-ing package
    cannot produce a maze, so the caller can handle the failure
    cleanly instead of crashing.
    """

    pass
