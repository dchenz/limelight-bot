lint:
	black --check .
	pylint *.py cogs database services tests
	pyright .

format:
	isort .
	black .

test:
	python3 -m unittest
