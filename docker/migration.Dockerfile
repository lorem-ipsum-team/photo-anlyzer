FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip install uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv venv -p 3.11
RUN . ./.venv/bin/activate
RUN uv sync --frozen

# Copy app for config. Other is for migration scripts
COPY app ./app
COPY alembic.ini ./
COPY migrations ./migrations

# Run migrations
CMD ["uv", "run", "alembic", "upgrade", "head"]
