PYTHON = python3
MANAGER = uv run
ARG = config.json

install:
	uv sync

run:
	--@$(MANAGER) $(PYTHON) pac-man.py $(ARG)

debug:
	@$(MANAGER) $(PYTHON) -m pdb pac-man.py

clean:
	@find . -type d -name __pycache__ -exec rm -rf {} +
	@find . -type d -name .mypy_cache -exec rm -rf {} +

deploy:
	@$(MANAGER) pyinstaller --onefile --name pac-man --add-data "assets:assets" pac-man.py

lint:
	@$(MANAGER) flake8 --exclude .venv .
	@$(MANAGER) mypy . --warn-return-any \
	--warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs \
	--check-untyped-defs

.PHONY: install run debug clean lint
