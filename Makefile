.DEFAULT_GOAL := help

.PHONY = help install install-pre-commit lint cp-env

ifneq (,$(wildcard ./config/.env))
    include config/.env
    export
endif

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo " ------------------- Setup commands ----------------------"
	@echo " help                 to show this message"
	@echo " install              to install dependencies"
	@echo " install-pre-commit   to install pre-commit hooks"
	@echo " lint                 to lint code with pre-commit hooks"
	@echo " cp-env               to copy .env.example to .env"
	@echo " ------------------- Django commands ---------------------"
	@echo " runserver            to run Django server"
	@echo " migrate              to run Django migrations"
	@echo " makemigrations       to make Django migrations"
	@echo " createsuperuser      to create Django superuser"
	@echo " shell                to run Django shell"
	@echo " ------------------- Docker commands ---------------------"
	@echo " docker-help          to show docker commands help message"
	@echo " build                to build containers"
	@echo " up                   to start containers"
	@echo " down                 to stop containers"
	@echo " down-v               to stop containers and remove volumes"
	@echo " restart              to restart containers"
	@echo " logs                 to show logs"
	@echo " docker-shell                to run shell in container"
	@echo " ------------------- Backup commands ---------------------"
	@echo " backups              to show database backups"
	@echo " backup               to backup database"
	@echo " ------------------- Testing commands --------------------"
	@echo " test                 to run tests"
	@echo " test-cov             to run tests with coverage"
	@echo " test-v               to run tests with verbose"
	@echo " test-app             to run tests for app"
	@echo " ------------------- Running commands --------------------"
	@echo " run-local            to run app locally"
	@echo " run-local-docker     to run app locally with docker"
	@echo " run-dev              to run app in development mode"
	@echo " run-prod             to run app in production mode"
	@echo " ---------------------------------------------------------"

install:
	@echo "SETUP: Installing dependencies..."
	poetry install

install-pre-commit:
	@echo "SETUP: Installing pre-commit hooks..."
	poetry run pre-commit install

lint:
	@echo "SETUP: Linting code..."
	poetry run pre-commit run --all-files

cp-env:
	@echo "SETUP: Copying .env.example to .env..."
	cp config/.env.example config/.env

# Django commands
.PHONY = runserver migrate makemigrations createsuperuser shell

RUN := $(if $(IN_DOCKER),python manage.py,poetry run python manage.py)

runserver:
	@echo "DJANGO: Running Django server..."
	$(RUN) runserver

migrate:
	@echo "DJANGO: Running Django migrations..."
	$(RUN) migrate

makemigrations:
	@echo "DJANGO: Making Django migrations..."
	$(RUN) makemigrations

createsuperuser:
	@echo "DJANGO: Creating Django superuser..."
	$(RUN) createsuperuser

shell:
	@echo "DJANGO: Running Django shell..."
	$(RUN) shell

makemessages:
	@echo "DJANGO: Making Django messages..."
	$(RUN) makemessages -l az -l en -l ru

compilemessages:
	@echo "DJANGO: Compiling Django messages..."
	$(RUN) compilemessages --ignore site-packages

# Testing commands
.PHONY = test test-cov test-v

app := core

test:
	@echo "TEST: Running tests..."
	poetry run pytest -v

test-cov:
	@echo "TEST: Running tests with coverage..."
	poetry run pytest --cov=server --cov-report=html

test-v:
	@echo "TEST: Running tests with verbose..."
	poetry run pytest -svv

test-app:
	@echo "TEST: Running tests for app..."
	poetry run pytest -v server/apps/$(app)

# Docker commands
.PHONY = docker-help build up down restart log

dev = -f docker-compose.yml -f docker/docker-compose.dev.yml --env-file config/.env --project-name ${PROJECT_NAME}
prod = -f docker-compose.yml -f docker/docker-compose.prod.yml --env-file config/.env --project-name ${PROJECT_NAME}

ENV ?= local

svc :=

docker-help:
	@echo "--------------------------------  Environment  ---------------------------------"
	@echo "To run the command for a specific environment run 'make ENV=<env> <target>'"
	@echo "or set ENV variable to <env> and run 'make <target>', where <env> is:"
	@echo "local:    the essential services to run the application locally (db, redis, etc)"
	@echo "dev:      the app in development mode (essential + django in development mode)"
	@echo "prod:     the app in production mode (essential + django in production mode)"
	@echo "----------------------------------  Service  -----------------------------------"
	@echo "To run the command for a specific service run 'make svc=<service> <target>'"
	@echo "where <service> is one of the services in docker compose file"
	@echo "--------------------------------------------------------------------------------"

build:
	@echo "DOCKER: Building containers..."
	docker compose $($(ENV)) build $(svc)

up:
	@echo "DOCKER: Starting containers..."
	docker compose $($(ENV)) up -d $(svc)

down:
	@echo "DOCKER: Stopping containers..."
	docker compose $($(ENV)) down $(svc)

down-v:
	@echo "DOCKER: Stopping containers with volumes..."
	docker compose $($(ENV)) down $(svc) -v

restart:
	@echo "DOCKER: Restarting containers..."
	docker compose $($(ENV)) restart $(svc)

log:
	@echo "DOCKER: Showing logs..."
	docker compose $($(ENV)) logs -f $(svc)

docker-shell:
	@echo "DOCKER: Running shell..."
	docker compose $($(ENV)) exec $(svc) sh

# Backup commands
.PHONY = check-prod backups backup

check-prod:
ifneq ($(ENV), prod)
	@echo "ERROR: You can't run this command in environment other than 'prod'"
	@exit 1
endif

backups: check-prod;
	@echo "BACKUP: Showing database backups..."
	docker compose $(prod) exec backup backups

backup: check-prod;
	@echo "BACKUP: Creating database backup..."
	docker compose $(prod) exec backup backup

# Run commands
.PHONY = run-local run-local-docker run-dev run-prod

run-local: migrate runserver;

run-local-docker:
	USE_POSTGRES=1 $(MAKE) -s up migrate runserver

run-dev: ENV=dev
run-dev: up

run-prod: ENV=prod
run-prod: up
