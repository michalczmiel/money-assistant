.PHONY: format test

all: format

format:
	black money_assistant

test:
	python manage.py test
