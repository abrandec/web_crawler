all: install test

install:
	python3 -m pip install -r requirements.txt

test:
	pytest -s ./tests/tests.py