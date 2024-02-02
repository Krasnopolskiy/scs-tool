FROM python:3.11

RUN pip install poetry

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD src src

ENTRYPOINT [ "python3", "src/main.py" ]
