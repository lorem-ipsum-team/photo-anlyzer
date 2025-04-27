FROM python:3.11-slim
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip install uv

# Install dependencies
COPY pyproject.toml uv.lock ./
RUN uv venv -p 3.11
RUN . ./.venv/bin/activate
RUN uv sync --frozen

# Run pre-install hooks
COPY hooks ./hooks
COPY app/internal/config/* ./app/internal/config/
RUN uv run python ./hooks/*.py

# Copy source and set entrypoint
COPY app ./app
CMD ["uv", "run", "python", "app/cmd/text_analyzer/main.py"]
