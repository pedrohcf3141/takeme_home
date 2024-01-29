FROM python:3.9-slim

ARG USER_ID=1000

RUN useradd --create-home --shell /bin/bash --uid $USER_ID user

WORKDIR /app

ENV PYTHONPATH "${PYTHONPATH}:/app"

RUN pip install poetry

COPY app/pyproject.toml /app/
COPY app/poetry.lock /app/

RUN poetry config virtualenvs.create false && poetry install --with=dev

COPY docker/entrypoint.sh /entrypoint/entrypoint.sh

COPY app /app

USER user

ENTRYPOINT ["/entrypoint/entrypoint.sh"]
