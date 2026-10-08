# Team Organization

## Team Members

The project was developed by:

- `abahoumi`
- `oatiya`

## Responsibilities

Responsibilities were divided according to GitHub Issues, branches, and Pull Requests.

| Area | Main contributor |
|---|---|
| Shared game state | abahoumi |
| UI and rendering | abahoumi |
| Player movement and animation | oatiya |
| Ghost movement and behavior | abahoumi |
| Maze generation and adapter | oatiya |
| Configuration | oatiya |
| Game progression | Both contributors |
| Scoring and highscores | Both contributors |
| Linting and type fixes | Both contributors |
| Integration and review | Both contributors |

This division was flexible. Contributors also reviewed and modified each other's work when integration required it.

## Decision-Making Process

Technical decisions were made by:

1. Creating or updating a GitHub Issue.
2. Describing the expected behavior.
3. Implementing the change in a branch.
4. Opening a Pull Request.
5. Reviewing the implementation.
6. Merging the Pull Request after integration.

## Handling Problems

Problems were handled through:

- New issues for missing features or bugs
- Follow-up Pull Requests
- Refactoring after integration
- Linting and type checking
- Manual testing of the affected feature

Examples include:

- Replacing the rendering geometry implementation
- Fixing flake8 errors
- Fixing mypy errors
- Adjusting ghost movement
- Integrating game progression with the UI

## Team Result

The team completed the main game features by working in parallel while using shared interfaces to limit integration problems.