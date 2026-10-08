# Project Decisions

This document records important technical decisions and the evidence supporting them.

Where the exact discussion was not preserved in the repository, the explanation is marked as an inference.

## Decision 1: Use a Python Graphics Library as the MLX-Compatible Rendering Layer

### Context

The project required a graphical rendering system comparable to the MLX interface used in the subject requirements.

### Decision

Use the graphical library already integrated into the Python project and expose rendering through the `src/ui/` and game rendering code.

### Rationale

- It allows the project to remain in Python.
- It supports windows, images, event handling, and screen rendering.
- It is already represented in the repository's dependency and UI implementation.

### Consequences

- Rendering logic is coupled to the selected Python graphics API.
- The UI must be tested manually in a graphical environment.
- A precise function-by-function MLX equivalence.

### Evidence

- [Issue #7 — Rendering skeleton and main menu](https://github.com/oualidAtiya/pac-man/issues/7)
- [PR #11 — Rendering skeleton and main menu](https://github.com/oualidAtiya/pac-man/pull/11)
- `src/ui/render.py`
- `src/ui/button.py`
- `src/ui/hud.py`

### Open Question

The repository does not currently contain a separate architecture document explicitly listing every MLX-equivalent function.

## Decision 2: Isolate the Maze Generator Behind an Adapter

### Context

The project uses the vendored `mazegenerator-2.1.0-py3-none-any.whl` package. The external package API and its README were not completely reliable for the required constructor behavior.

### Decision

Use `src/maze/adapter.py` as the boundary between the external package and the rest of the game.

### Rationale

- The rest of the game should use the project's own `Maze` and `Cell` models.
- External API changes should be isolated to one location.
- Special `"42"` cells need to remain distinguishable from normal walls.

### Consequences

- The adapter must remain the only direct integration point.
- Deterministic generation and special-cell handling require dedicated testing.
- Future generator replacement should affect fewer files.

### Evidence

- [Issue #6 — Maze adapter](https://github.com/oualidAtiya/pac-man/issues/6)
- `src/maze/adapter.py`
- `src/maze/cell.py`
- `src/maze/maze.py`
- `mazegenerator-2.1.0-py3-none-any.whl`

## Decision 3: Replace Rect/Subsurface Usage with a Simpler Rect Abstraction

### Context

A refactoring was needed around UI geometry and rendering compatibility.

### Decision

Replace the previous subsurface-based approach with a simpler rectangle abstraction supporting the required geometry operations.

### Rationale

- Reduce dependency on behavior that was difficult to type or port.
- Make positioning operations such as `centerx` and `centery` explicit.
- Improve compatibility with static analysis.

### Consequences

- Existing drawing code needed to be updated.
- Geometry behavior must be checked visually after refactoring.
- The custom abstraction should remain small and focused.

### Evidence

- [PR #50 — Drop subsurface usage and implement simple Rect](https://github.com/oualidAtiya/pac-man/pull/50)
- `src/ui/utils.py`
- `src/ui/render.py`

## Decision 4: Store Ghost Sprites as Separate Assets

### Context

Ghosts have different colors and behavior states.

### Decision

Use separate image assets for the ghost variants already stored under `assets/images/ghosts/`.

### Rationale

- It keeps rendering code simple.
- Each ghost color can be selected directly.
- Frightened states can use dedicated blue or scared assets.

### Consequences

- Asset naming and loading paths must remain stable.
- Rendering tests must cover normal, frightened, and eaten states.
- The repository contains more image files but less runtime sprite-sheet logic.

### Evidence

- [Issue #19 — Ghost rendering and animation](https://github.com/oualidAtiya/pac-man/issues/19)
- `assets/images/ghosts/`
- `src/game/ghost.py`
- `src/ui/render.py`

## Decision 5: Use a Shared GameState

### Context

The logic and rendering portions of the project needed a stable interface for communication.

### Decision

Use a shared game-state model containing the screen state and game entities.

### Rationale

- UI code can render the current state without owning gameplay logic.
- Game logic can update entities without directly drawing them.
- Teams can work in parallel against the same data contract.

### Consequences

- Changes to shared state affect both gameplay and rendering.
- State transitions must be tested carefully.
- The model becomes a central integration point.

### Evidence

- [Issue #4 — Define shared game-state interface](https://github.com/oualidAtiya/pac-man/issues/4)
- [PR #8 — Define the shared game state](https://github.com/oualidAtiya/pac-man/pull/8)
- `src/game/state.py`

## Decision 6: Use Mouse-Oriented Menu Interaction

### Context

The UI contains image-based menu buttons such as Start, High Scores, Instructions, Resume, Back, and Exit.

### Decision

Use button-based menu interaction through the UI layer.

### Rationale

- The existing assets are designed as normal, hover, and pressed button images.
- It provides a clear interaction model for menu screens.
- It separates menu navigation from in-game keyboard movement.

### Consequences

- Menu interaction must be tested with mouse events.
- The packaged build needs clear instructions for menu and gameplay controls.
- Keyboard-only accessibility may be limited.

### Evidence

- `src/ui/button.py`
- `assets/images/buttons/`
- [PR #11 — Rendering skeleton and main menu](https://github.com/oualidAtiya/pac-man/pull/11)
- [PR #38 — Instruction, highscores, and pause screens](https://github.com/oualidAtiya/pac-man/pull/38)