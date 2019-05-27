.PHONY: dev shell check test{% if cookiecutter.use_database == 'y' %} migrate upgrade dbshell{% endif %}

COMPOSE-DEV = docker-compose -f docker-compose.yml -f docker-compose.dev.yml
COMPOSE-TEST = docker-compose -f docker-compose.yml -f docker-compose.test.yml
FILE = $(file)

dev:
	if [ ! -f .env ]; then touch .env; fi;
	$(COMPOSE-DEV) up --build

shell:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} python cli.py run_shell

check:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} python cli.py check_apispec

test:
	if [ ! -f .env ]; then touch .env; fi;
	TEST_FILE=$(FILE) $(COMPOSE-TEST) up --build --abort-on-container-exit
{% if cookiecutter.use_database == 'y' %}
migrate:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} alembic revision --autogenerate

upgrade:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} alembic upgrade head

dbshell:
	$(COMPOSE-DEV) exec {{cookiecutter.app_name}} python cli.py dbshell
{% endif %}