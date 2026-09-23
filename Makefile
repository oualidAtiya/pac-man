PYTHON = python3
MANAGER = uv run

install:
	uv sync

run:
	@$(MANAGER) $(PYTHON) pac-man.py config.json

debug:
	@$(MANAGER) $(PYTHON) pdb pac-man.py

clean:
	@rm -rf src/__pycache__ .mypy_cache

lint:
	@$(MANAGER) flake8 .
	@$(MANAGER) mypy . --warn-return-any
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
	--check-untyped-defs

.PHONY: install run debug clean lint