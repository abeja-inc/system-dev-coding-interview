.PHONY: dev run format lint test test-user docker-build docker-run

PYTHON_VERSION?=3.13
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

format: format-fix lint-fix

lint-fix:
	uv run ruff check --fix .

format-fix:
	uv run ruff format .

lint: format-check lint-check mypy

format-check:
	uv run ruff format --check .

lint-check:
	uv run ruff check .

mypy:
	uv run mypy . --config-file ./pyproject.toml

docker-build:
	docker image build --no-cache --tag ${IMAGE_NAME} . --build-arg PYTHON_VERSION=${PYTHON_VERSION}

docker-run:
	docker container run -it -v ${VOLUME} --rm ${IMAGE_NAME}
