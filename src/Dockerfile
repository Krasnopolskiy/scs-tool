FROM python:3.11

RUN pip install poetry

COPY ./pyproject.toml pyproject.toml

COPY ./poetry.lock poetry.lock

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD . .

ENTRYPOINT [ "python3", "main.py" ]
