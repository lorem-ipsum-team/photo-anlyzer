FROM python:3.13-slim
WORKDIR /app
ENV PYTHONPATH=/app
RUN pip install uv

COPY pyproject.toml uv.lock ./
RUN uv venv -p 3.13
RUN . ./.venv/bin/activate
RUN uv sync --frozen

COPY app ./app

CMD ["uv", "run", "python", "app/cmd/photo_analyzer/main.py"]
