# Risk Analysis

| Risk | Possible impact | Mitigation | Result |
|---|---|---|---|
| External maze package behaves differently than expected | Maze generation could fail | Use a dedicated maze adapter | Mitigated |
| Game logic and rendering interfaces become incompatible | Integration delays | Define shared interfaces early | Mitigated |
| Player movement crosses walls | Gameplay becomes incorrect | Reuse maze collision rules | Mitigated |
| Ghost behavior becomes difficult to manage | Ghosts may not chase or flee correctly | Use explicit ghost behavior states | Mitigated |
| Game-state transitions become inconsistent | Victory, pause, or game-over screens may fail | Centralize screen states in `GameState` | Mitigated |
| Highscore file is missing or invalid | The game may crash while loading scores | Validate score data and handle errors | Mitigated |
| Static-analysis errors accumulate | Final cleanup becomes difficult | Run flake8 and mypy before completion | Mitigated |
| UI changes break existing screens | Menus or buttons may stop working | Make UI changes through focused Pull Requests | Mitigated |
| Different development branches conflict | Features may be difficult to merge | Use small branches and incremental integration | Mitigated |

## Final Risk Assessment

The main technical risks were identified during development and addressed through:

- Abstraction boundaries
- Shared interfaces
- Incremental Pull Requests
- Manual testing
- Refactoring
- Static analysis