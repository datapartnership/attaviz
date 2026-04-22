.PHONY: install format lint test clean \
        docs-preview docs-render docs-publish docs-clean

install:
	uv sync --dev

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest

docs-preview:
	uv run quarto preview docs/

docs-render:
	uv run quarto render docs/

docs-publish:
	uv run quarto publish gh-pages docs/ --no-prompt --no-browser

docs-clean:
	rm -rf docs/_site docs/.quarto docs/_freeze

clean: docs-clean
	rm -rf dist build .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
