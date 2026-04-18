.PHONY: install format lint test notebook clean

install:
	uv sync --dev

format:
	uv run ruff format .

lint:
	uv run ruff check .

test:
	uv run pytest

notebook:
	uv run jupyter notebook examples/gallery.ipynb

clean:
	rm -rf dist build .pytest_cache .ruff_cache
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
