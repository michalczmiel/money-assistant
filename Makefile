.PHONY: format test lint dev

all: format lint

dev:
	cd .docker && docker-compose up db api redis worker

format:
	black money_assistant

test:
	python manage.py test

lint:
	flake8 money_assistant
