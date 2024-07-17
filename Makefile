.PHONY: docker-apply-db-migrations
docker-apply-db-migrations:
	docker-compose run --rm app alembic upgrade head

.PHONY: docker-build
docker-build:
	docker-compose build

.PHONY: docker-clean
docker-clean:
	docker-compose down -v --remove-orphans | true
	docker-compose rm -f | true
	docker volume rm app_api_py_postgresql_data | true

.PHONY: docker-create-db-migration
docker-create-db-migration:
	docker-compose up -d db | true
	docker-compose run --no-deps app alembic revision --autogenerate -m "$(msg)"

.PHONY: docker-up
docker-up:
	docker-compose up --remove-orphans

.PHONY: setup
setup:
	pyenv local
	python -m venv .venv
	cd .venv/bin && source activate
	.venv/bin/pip install -U pip setuptools ipykernel
	.venv/bin/pip install poetry
	.venv/bin/poetry env use `pyenv which python`
	.venv/bin/poetry install
