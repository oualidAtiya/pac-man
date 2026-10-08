# Project Analysis and Choices

## Project Approach

The project was developed incrementally. Core interfaces were defined first, followed by the maze, rendering, gameplay, user interface, scoring, and cleanup.

This order allowed the two contributors to work on different parts of the project while sharing common models.

## Main Technical Choices

### Shared GameState

A shared `GameState` object was used to contain:

- Current screen
- Maze
- Player
- Ghosts
- Pac-gums
- Level
- Timers
- Scores

This made communication between game logic and rendering easier.

### Maze Adapter

The external maze generator is accessed through `src/maze/adapter.py`.

This prevents the rest of the game from depending directly on the external package API. The internal code uses its own maze and cell models.

### Pygame Rendering

Pygame was used for:

- Window creation
- Image loading
- Event handling
- Rendering
- Game-loop support

The UI code is separated into its own `src/ui/` package.

### Separate Game and UI Logic

Game rules are stored mainly in `src/game/`, while drawing and interaction are handled in `src/ui/`.

This separation makes the code easier to update and debug.

### JSON Configuration

The configuration is stored in `config.json`.

JSON was chosen because it is:

- Easy to edit
- Easy to validate
- Human-readable
- Suitable for a small game project

### JSON Highscores

Highscores are stored in JSON because the project only needs a small local list of scores. A database would add unnecessary complexity.

## Project Management Choices

GitHub Issues were used to define tasks and acceptance criteria.

Pull Requests were used to:

- Review changes
- Separate features
- Fix integration problems
- Keep the main branch stable

The project was completed through several small feature additions instead of one large implementation.