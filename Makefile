SOURCES = $(shell git diff --name-only --diff-filter=AM HEAD | grep -E '\.py$$')

lint:
	poetry run pylint $(SOURCES)

format:
	poetry run black $(SOURCES)
	poetry run isort $(SOURCES)
