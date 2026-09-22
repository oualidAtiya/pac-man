PYTHON = python3
MANAGER = uv run

install:
	uv sync

run:
	@$(MANAGER) $(PYTHON) -m src

debug:
	@$(MANAGER) $(PYTHON) -m pdb -m src

clean:
	@rm -rf src/__pycache__ .mypy_cache

lint:
	@$(MANAGER) flake8 src/.
	@$(MANAGER) mypy src/. --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

.PHONY: install run debug clean lint