run-tests:
	python -m unittest discover tests

test-coverage:
	coverage run --source=. -m unittest discover -s tests/
	coverage report -m

webdriver:
	./scripts/get-driver
