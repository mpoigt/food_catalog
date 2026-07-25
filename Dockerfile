FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app/src

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --without dev --no-interaction --no-ansi

COPY . .

RUN chmod +x entrypoint.sh

CMD ["./entrypoint.sh"]