# Blocking Points and Conflicts

## Maze Package Documentation Conflict

The maze package documentation and its actual constructor behavior were not completely consistent.

### Solution

The project introduced a maze adapter in:

```text
src/maze/adapter.py
```

This keeps the external package details in one place and provides the rest of the game with an internal maze model.

## Rendering Integration Problems

Some rendering operations created compatibility and typing problems during development.

### Solution

The rendering code was refactored to use a simpler rectangle approach. Follow-up Pull Requests were used to fix related flake8 and mypy errors.

## Shared Interface Changes

Game logic and rendering needed to use the same data structures.

### Solution

The shared game-state interface was created early. Later changes were integrated through focused Pull Requests instead of changing multiple parts of the project without review.

## Branch Integration Conflicts

Some features depended on changes made in other branches, especially:

- Player and maze integration
- Ghost and player interactions
- Game progression
- Rendering and game-state updates

### Solution

The team used:

- Small feature branches
- Pull Requests
- Incremental merges
- Follow-up fixes after integration

## Final Status

No unresolved blocker prevented completion of the main game implementation.

The project was completed through incremental implementation, review, testing, and refactoring.