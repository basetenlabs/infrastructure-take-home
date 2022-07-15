.PHONY: all mock_server start migrate lint install

all: install start

install:
	poetry install

start:
	poetry run uvicorn baseten_infra_take_home.main:app --reload

remote_endpoint:
	poetry run uvicorn baseten_infra_take_home.remote_server:app --reload --port=8001

lint:
	poetry run black **/*.py
	poetry run flake8
