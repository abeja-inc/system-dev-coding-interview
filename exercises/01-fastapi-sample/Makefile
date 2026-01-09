.PHONY: dev run format lint test test-user docker-build docker-run

PYTHON_VERSION?=3.8
IMAGE_NAME=abeja-coding-interview-sql-app:test
VOLUME=$(PWD)/sql_app:/app/sql_app

dev:
	uv run uvicorn sql_app.main:app --reload

run:
	uv run uvicorn sql_app.main:app --host 0.0.0.0 --port 8000

test: test-user test-integration

test-user:
	uv run pytest

test-integration:
	uv run pytest .integration

format: black ruff-fix

ruff-fix:
	uv run ruff --fix .

black:
	uv run black .

lint: black-check ruff-check mypy

black-check:
	uv run black --check .

ruff-check:
	uv run ruff check .

mypy:
	uv run mypy . --config-file ./pyproject.toml

docker-build:
	docker image build --no-cache --tag ${IMAGE_NAME} . --build-arg PYTHON_VERSION=${PYTHON_VERSION}

docker-run:
	docker container run -it -v ${VOLUME} --rm ${IMAGE_NAME}
