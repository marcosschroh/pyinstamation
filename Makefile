init: webdriver install-deps start-conf

install-deps:
	@echo "Installing dependencies..."
	pip install -r requirements.txt
	@echo "Done.\n"

start-conf:
	@echo "Creating new configuration file..."
	@cp ./default.config.yaml ./config.yaml
	@echo "Done."

run-bot:
	python -m pyinstamation

run-tests-coverage:
	coverage run --source=pyinstamation -m unittest discover -s tests/
	coverage report -m

webdriver:
	@echo "Retrieving selenium webdriver..."
	./scripts/get-driver
	@echo "Done.\n"
