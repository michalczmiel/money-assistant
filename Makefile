.PHONY: format test lint

all: format

format:
	black money_assistant

test:
	python manage.py test

lint:
	flake8 money_assistant
