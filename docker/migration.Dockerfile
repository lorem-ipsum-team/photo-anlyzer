FROM python:3.13-alpine
WORKDIR /app
ENV PYTHONPATH=/app
RUN apk add uv

COPY pyproject.toml uv.lock ./
RUN uv venv -p 3.13
RUN source ./.venv/bin/activate
RUN uv sync --frozen

COPY app ./app
COPY alembic.ini ./
COPY migrations ./migrations

CMD ["uv", "run", "alembic", "upgrade", "head"]
