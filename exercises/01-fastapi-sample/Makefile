.PHONY: dev run format lint test

dev:
	poetry run uvicorn sql_app.main:app --reload

run:
	poetry run uvicorn sql_app.main:app --host 0.0.0.0 --port 8000

format:
	poetry run pysen run format

lint:
	poetry run pysen run lint

test:
	poetry run pytest