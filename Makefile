lint:
	black --check .
	pylint *.py cogs database services tests graphapi
	pyright .

format:
	isort .
	black .

test:
	python3 -m unittest
