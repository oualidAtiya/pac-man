PYTHON = python3
MANAGER = uv run

install:
	uv sync

run:
	@$(MANAGER) $(PYTHON) pac-man.py config.json

debug:
	@$(MANAGER) $(PYTHON) pdb pac-man.py

clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	@$(MANAGER) flake8 pac-man.py src/.
	@$(MANAGER) mypy src/. --warn-return-any
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
	--check-untyped-defs

.PHONY: install run debug clean lint