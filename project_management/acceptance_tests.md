# Acceptance Test Plan

| Feature | Test | Expected result | Result | Bugs or fixes |
|---|---|---|---|---|
| Installation | Run `make install` | Dependencies are installed | Passed during development | None recorded |
| Startup | Run `make run` | Game window opens | Passed during development | Configuration handling was added |
| Configuration | Use valid and invalid configuration values | Invalid values are handled safely | Passed during development | Config validation added |
| Maze generation | Start the game with a configured seed | A maze is generated and displayed | Passed during development | Maze adapter added |
| Maze collision | Move toward walls | Player cannot move through walls | Passed during development | Movement logic refined |
| Player movement | Use movement controls in all directions | Player moves correctly | Passed during development | Smooth movement added |
| Player animation | Move and stop the player | Animation changes while moving | Passed during development | Animation integrated |
| Ghost chase | Play near normal ghosts | Ghosts move toward the player | Passed during development | Ghost movement refined |
| Ghost flee | Eat a super pac-gum | Ghosts enter frightened mode | Passed during development | Timer behavior added |
| Ghost collision | Touch ghosts in different states | Correct score or life behavior occurs | Passed during development | Collision logic integrated |
| Pac-gums | Collect normal and super pac-gums | Score and game state update correctly | Passed during development | Pac-gum handling added |
| HUD | Play a game | Score, lives, level, and timers are visible | Passed during development | HUD added |
| Level progression | Collect all required pac-gums | Next level starts correctly | Passed during development | Game progression added |
| Victory | Complete the victory condition | Victory screen appears | Passed during development | Victory flow integrated |
| Game over | Lose all lives | Game-over screen appears | Passed during development | Game-over flow integrated |
| Name entry | Enter valid and invalid names | Invalid characters and long names are rejected | Passed during development | Input validation added |
| Highscores | Save and reopen a score | Score is displayed in the highscore screen | Passed during development | Persistence added |
| Invalid highscores | Use invalid score data | Invalid data does not crash the game | Passed during development | Validation and error handling added |
| Main menu | Navigate through menu options | Buttons open the correct screens | Passed during development | Menu screens integrated |
| Pause screen | Pause and resume the game | Game pauses and resumes correctly | Passed during development | Pause screen added |
| Linting | Run `make lint` | flake8 and mypy complete successfully | Passed during development | Lint and type fixes merged |

## Final Acceptance Result

The main game features were tested during development and completed.

The acceptance tests covered:

- Installation
- Configuration
- Maze generation
- Movement
- Ghost behavior
- Collisions
- Game progression
- User interface
- Highscores
- Code quality