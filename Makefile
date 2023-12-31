lint:
	black --check .
	pylint *.py cogs database model services tests
	pyright .

format:
	isort .
	black .

test:
	python3 -m unittest
