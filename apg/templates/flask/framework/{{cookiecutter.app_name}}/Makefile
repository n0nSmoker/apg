.PHONY: dev build up stop migrate upgrade shell bash dbshell redis-cli test db


COMPOSE-PROD = docker-compose -f docker-compose.yml
COMPOSE-DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE-TEST = docker-compose -f docker-compose.yml -f docker-compose.test.yml
FILE = $(file)

dev:
	if [ ! -f .env ]; then touch .env; fi;
	$(COMPOSE-DEV) up --build

build:
	$(COMPOSE-DEV) build

up:
	$(COMPOSE-PROD) up

stop:
	$(COMPOSE-DEV) down

migrate:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} flask db migrate

upgrade:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} flask db upgrade

shell:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} flask debug

bash:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} /bin/sh

dbshell:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} flask dbshell

redis-cli:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}}-redis redis-cli

test:
	if [ ! -f .env ]; then touch .env; fi;
	TEST_FILE=$(FILE) $(COMPOSE-TEST) up --build --scale {{cookiecutter.app_name}}-redis=0 --abort-on-container-exit

db:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} flask db init
