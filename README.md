*This project has been created as part of the 42 curriculum by abahoumi, oatiya.*

# Pac-Man

## Description

This project is a Python implementation of a Pac-Man-style game developed as part of the 42 curriculum.

The goal is to create a playable game with:

- A procedurally generated maze
- A controllable Pac-Man player
- Four ghosts with different behavior states
- Pac-gums and super pac-gums
- Collision detection
- Lives, scoring, levels, and timers
- Menu, pause, instructions, victory, and game-over screens
- Persistent highscores
- Configurable gameplay parameters

The game is implemented in Python and uses Pygame for graphics and input handling. The project also uses a local version of the `mazegenerator` package to generate mazes.

## Play the Game

You can dowload and play the packaged version of the game on itch.io:
[Play Pac-Man](https://oualidatiya.itch.io/pac-man)


## Features

- Main menu with Start, Highscores, Instructions, and Exit options
- Maze rendering based on generated maze data
- Smooth Pac-Man movement with wall collision
- Pac-Man directional animation
- Ghost chase, flee, and respawn behavior
- Super pac-gum frightened mode
- Player-ghost collision handling
- Player death animation
- Multiple levels
- Victory and game-over screens
- HUD displaying score, lives, level, and timers
- Name entry after a qualifying score
- Persistent highscore file
- Configurable game rules
- Static analysis with `flake8` and `mypy`

## Instructions

### Requirements

- Python 3.10 or newer
- `uv`
- A graphical environment capable of running Pygame

The required Python version and dependencies are declared in [`pyproject.toml`](pyproject.toml).

### Installation

Clone the repository and install the dependencies:

```bash
make install
```

This runs:

```bash
uv sync
```

The project uses the local package:

```text
mazegenerator-2.1.0-py3-none-any.whl
```

### Running the Game

Run the game with the default configuration:

```bash
make run
```

This executes:

```bash
uv run python3 pac-man.py config.json
```

The application entry point is [`pac-man.py`](pac-man.py).

### Debugging

The project provides a debugging command:

```bash
make debug
```

### Cleaning Generated Python Files

To remove Python cache directories:

```bash
make clean
```

### Linting

Run the required static-analysis checks with:

```bash
make lint
```

This runs:

- `flake8`
- `mypy`

The exact commands are defined in [`Makefile`](Makefile).

## Configuration

The default configuration file is [`config.json`](config.json).

The configuration is loaded by [`src/config/loader.py`](src/config/loader.py) and represented by the Pydantic models in [`src/config/models.py`](src/config/models.py).

### Configuration Fields

| Field | Type | Default | Description |
|---|---|---:|---|
| `lives` | integer | `3` | Number of player lives |
| `seed` | integer | `42` | Seed used for maze generation |
| `super_gum_time` | integer | `10` | Duration of the frightened ghost state |
| `level_max_time` | integer | `60` | Maximum time allowed for a level |
| `points_per_pacgum` | integer | `10` | Points awarded for a normal pac-gum |
| `points_per_super_pacgum` | integer | `20` | Points awarded for a super pac-gum |
| `points_per_ghost` | integer | `30` | Points awarded for eating a frightened ghost |
| `highscore_filename` | string | `highscores.json` | File used to store highscores |

The default values are defined in [`src/config/models.py`](src/config/models.py).

### Configuration Validation

Configuration values are validated when the file is loaded:

- Unknown keys are ignored.
- Missing values use their defaults.
- Invalid numeric values are replaced with safe defaults.
- The highscore filename must be a JSON filename.
- Configuration errors are logged instead of producing an uncontrolled traceback.

The repository's current example configuration uses customized values, including:

```json
{
  "lives": 5,
  "seed": 96,
  "points_per_pacgum": 70,
  "points_per_super_pacgum": 80,
  "points_per_ghost": 90,
  "super_gum_time": 60,
  "level_max_time": 120
}
```

The configuration loader also supports the comment format used in the provided configuration file.

## Highscore

Highscores are implemented in [`src/game/score.py`](src/game/score.py).

Each score contains:

- A player name
- A numeric score

Player names are validated according to the following rules:

- Only letters, numbers, and spaces are accepted.
- Names are limited to ten characters.
- Scores must be positive.
- Unexpected fields are rejected.

Scores are saved as JSON in the file configured by `highscore_filename`. The default file is [`highscores.json`](highscores.json).

When scores are loaded:

1. The file is parsed as JSON.
2. Each entry is validated.
3. Invalid or malformed data is handled without crashing the game.
4. Valid scores are sorted from highest to lowest.

The highscore system uses JSON because it is simple, human-readable, and easy to inspect or edit during development. It also avoids introducing a database dependency for a small standalone game.

The game includes a name-entry flow after a game ends. The player can enter a validated name, confirm it, and return to the menu. Highscores can then be viewed from the Highscores screen.

The project requirements describe a persistent top-ten highscore system. The current implementation provides validation, persistence, and sorting; the final top-ten limit should be confirmed during final acceptance testing.

## Maze Generation

Maze generation is implemented through the local `mazegenerator` package:

```text
mazegenerator-2.1.0-py3-none-any.whl
```

The dependency is configured in [`pyproject.toml`](pyproject.toml):

```toml
[tool.uv.sources]
mazegenerator = { path = "mazegenerator-2.1.0-py3-none-any.whl" }
```

The project does not expose the external package directly to the rest of the game. Instead, [`src/maze/adapter.py`](src/maze/adapter.py) provides a boundary around the package.

The adapter creates a maze using:

```python
MazeGenerator(
    size=(width, height),
    seed=seed,
)
```

The generated numeric maze values are converted into the project's own `Cell` objects. The rest of the application works with the internal maze model rather than directly depending on the external package API.

This design provides:

- A stable internal maze interface
- Isolation from external package changes
- A single location for maze-generator integration
- Support for deterministic maze generation using a seed
- A place to handle special maze cells, including the `42` pattern required by the project

The main maze modules are:

- [`src/maze/adapter.py`](src/maze/adapter.py)
- [`src/maze/cell.py`](src/maze/cell.py)
- [`src/maze/maze.py`](src/maze/maze.py)
- [`src/maze/generator_error.py`](src/maze/generator_error.py)

## Implementation

The project is organized into several main layers.

### Application Entry Point

[`pac-man.py`](pac-man.py) starts the application, loads the configuration, creates the game objects, and runs the main game loop.

### Configuration Layer

The configuration layer is located in [`src/config/`](src/config/).

It contains:

- `loader.py` — reads and parses the configuration file
- `models.py` — defines validated configuration models
- `logger.py` — provides logging and error-reporting helpers

### Game Logic Layer

The game logic is located in [`src/game/`](src/game/).

Important modules include:

- `direction.py` — movement directions
- `player.py` — player position, movement, lives, score, and respawning
- `ghost.py` — ghost movement and behavior states
- `pacgum.py` — normal and super pac-gum handling
- `score.py` — highscore validation, loading, and saving
- `state.py` — shared game state and screen transitions

### Maze Layer

The maze layer is located in [`src/maze/`](src/maze/).

It converts the generated maze into internal objects that can be used by the player, ghosts, and renderer.

### User Interface Layer

The UI layer is located in [`src/ui/`](src/ui/).

It contains:

- `render.py` — game and screen rendering
- `button.py` — menu buttons and interaction
- `hud.py` — score, lives, level, and timer display
- `text_box.py` — text-entry and message display
- `utils.py` — UI geometry and rendering helpers

### Assets

Game images are stored in [`assets/`](assets/), including:

- Pac-Man animation frames
- Ghost sprites
- Maze components
- Buttons
- HUD images
- Menu and game-state screens
- Digits and letters

## General Software Architecture

The project follows a layered architecture.

```text
pac-man.py
    |
    +-- Configuration
    |     +-- Config loader
    |     +-- GameConfig
    |
    +-- GameState
    |     +-- Screen
    |     +-- Maze
    |     +-- Player
    |     +-- Ghosts
    |     +-- Pacgum
    |     +-- Scores
    |
    +-- Maze
    |     +-- MazeAdapter
    |     +-- Maze
    |     +-- Cell
    |
    +-- Game Logic
    |     +-- Player
    |     +-- Ghost
    |     +-- Pacgum
    |     +-- Score
    |
    +-- User Interface
          +-- Renderer
          +-- Buttons
          +-- HUD
          +-- TextBox
```

### `GameState`

[`GameState`](src/game/state.py) acts as the composition root of the application. It stores the objects required to update and render a frame:

- Current screen
- Maze
- Player
- Ghosts
- Pac-gums
- Current level
- Remaining time
- Super pac-gum timer
- Scores

`GameState` also coordinates:

- Level transitions
- Respawning
- Pac-gum consumption
- Ghost frightened mode
- Player-ghost collisions
- Victory and game-over transitions

### `Player`

The player is responsible for:

- Position and direction
- Movement
- Wall collision
- Eating pac-gums
- Score updates
- Losing lives
- Respawning
- Animation state

### `Ghost`

Ghosts are responsible for:

- Position and movement
- Chase behavior
- Flee behavior
- Eaten behavior
- Respawning
- Direction and rendering state

### `Maze`

The maze model provides the internal representation used by the player and ghosts. It hides the external maze-generator implementation behind the adapter.

### `Renderer`

The renderer reads the shared `GameState` and draws the current screen. The renderer does not own the core gameplay rules.

## Technical Choices

### Pygame

Pygame is used for:

- Creating the game window
- Loading and displaying images
- Processing input events
- Managing the game loop
- Drawing the user interface

### Pydantic

Pydantic is used to validate:

- Configuration data
- Highscore entries
- Player names
- Score values

### `uv`

`uv` is used for dependency installation and command execution. It provides reproducible project setup through `pyproject.toml` and `uv.lock`.

## Resources

### Classic References

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame Sprite and Surface Tutorials](https://www.pygame.org/docs/ref/surface.html)

### AI Usage

AI assistance was used for project-support activities, including:

- Organizing the README structure according to the project requirements
- Reviewing the repository structure and identifying relevant modules
- Preparing project-management documentation
- Summarizing GitHub Issues and Pull Requests
- Preparing acceptance-test tables
- Identifying remaining risks, blockers, and documentation gaps
- Improving the clarity of technical explanations

AI assistance was not used as a substitute for understanding or validating the project. Implementation decisions, repository changes, testing, and final verification remain the responsibility of the project team.

## Project Management

Project-management documents are available in the [`project_management/`](project_management/) directory.

The directory contains:

- [Project management overview](project_management/README.md)
- [Timeline](project_management/timeline.md)
- [Progress tracking](project_management/progress.md)
- [Technical decisions](project_management/decisions.md)
- [Risk analysis](project_management/risks.md)
- [Team organization](project_management/team.md)
- [Acceptance tests](project_management/acceptance_tests.md)
- [Blockers and conflicts](project_management/blockers.md)

The project was managed using GitHub Issues, feature branches, Pull Requests, code review, and incremental integration into the `main` branch.
