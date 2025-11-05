FROM python:3.10-slim
WORKDIR /app
COPY pyproject.toml .
COPY src/logger/ .
RUN apt-get update && apt-get install -y curl && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    export PATH="$HOME/.local/bin:$PATH" && \
    uv sync
ENV PATH="$HOME/.local/bin:$PATH"
CMD ["/root/.local/bin/uv", "run", "python", "logger.py"]
