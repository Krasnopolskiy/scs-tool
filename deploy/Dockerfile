FROM python:3.11

ENV PATH="${PATH}:/root/.cargo/bin"

RUN curl https://sh.rustup.rs -sSf | sh -s -- -y

RUN pip install poetry

COPY pyproject.toml .

COPY poetry.lock .

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-root --no-cache

ADD src src
