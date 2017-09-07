webdriver:
	./scripts/get-driver

start-conf:
	cp ./default.config.yaml ./config.yaml

run-bot:
	python -m pyinstamation

run-tests-coverage:
	coverage run --source=pyinstamation -m unittest discover -s tests/
	coverage report -m

init: webdriver start-conf