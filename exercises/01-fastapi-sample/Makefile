.PHONY: dev run format lint test docker-build docker-run

PYTHON_VERSION?=3.8
IMAGE_NAME=abeja-coding-interview-sql-app:test
VOLUME=./sql_app:/app/sql_app

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

lint: black-check ruff-check mypy

black-check:
	poetry run black --check .

ruff-check:
	poetry run ruff check .

mypy:
	poetry run mypy . --config-file ./pyproject.toml

docker-build:
	docker image build --no-cache --tag ${IMAGE_NAME} . --build-arg PYTHON_VERSION=${PYTHON_VERSION}

docker-run:
	docker container run -it -v ${VOLUME} --rm ${IMAGE_NAME}
