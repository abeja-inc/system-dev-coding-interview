.PHONY: dev run format lint test

dev:
	poetry run uvicorn sql_app.main:app --reload

run:
	poetry run uvicorn sql_app.main:app --host 0.0.0.0 --port 8000

test:
	poetry run pytest

format: black ruff-fix

ruff-fix:
	poetry run ruff --fix .

black:
	poetry run black .

lint: black-check ruff-check

black-check:
	poetry run black --check .

ruff-check:
	poetry run ruff check .
