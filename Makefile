SOURCES = $(shell git ls-files '*.py')

lint:
	pylint --rcfile=pylint.toml $(SOURCES)

format:
	black $(SOURCES)
	isort $(SOURCES)
