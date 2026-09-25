# Contributing to Attaviz

Thank you for improving Attaviz. You can report bugs, propose features, improve
documentation, or submit code through the
[GitHub repository](https://github.com/datapartnership/attaviz).

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) in all project spaces.

## Report an issue

Open a GitHub issue and include:

- what you expected;
- what happened instead;
- a minimal example, when possible;
- your Python, Altair, and Attaviz versions.

For feature requests, describe the publishing or visualization problem before
proposing an interface.

## Set up the project

Install [uv](https://docs.astral.sh/uv/), then clone and sync the repository:

```bash
git clone https://github.com/datapartnership/attaviz.git
cd attaviz
uv sync --all-groups
```

## Run the checks

Run the test, lint, and formatting checks before opening a pull request:

```bash
uv run pytest -q
uv run ruff check .
uv run ruff format --check .
```

To apply formatting locally:

```bash
uv run ruff format .
```

## Build the documentation

Install [Quarto](https://quarto.org/docs/get-started/), then render the site:

```bash
quarto render docs
```

The generated site is written to `docs/_site/` and is not committed.

Documentation examples should use local or packaged data so builds do not
depend on remote services.

## Open a pull request

Create a focused branch, commit the smallest complete change, and open a pull
request against `main`. Explain the problem, the chosen solution, and the checks
you ran. Link related issues when applicable.

By contributing, you agree that your work is licensed under the repository's
[MPL-2.0 license](../LICENSE).
