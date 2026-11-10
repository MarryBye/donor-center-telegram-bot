# Multi-stage Dockerfile for Kharkiv Donor Center Telegram Bot
FROM ghcr.io/astral-sh/uv:latest AS uv_bin

FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy

WORKDIR /app

# Copy uv binary
COPY --from=uv_bin /uv /uvx /bin/

# Install dependencies using uv frozen lockfile
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-dev --no-install-project

# Runtime stage
FROM python:3.12-slim AS runner

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

WORKDIR /app

# Create unprivileged application user
RUN groupadd -r appgroup && useradd -r -g appgroup -d /app appuser

# Copy virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy application source files
COPY --chown=appuser:appgroup bot/ bot/
COPY --chown=appuser:appgroup src/ src/
COPY --chown=appuser:appgroup bot_app.py config.py handlers_imports.py keyboards_imports.py pyproject.toml ./

# Ensure runtime cache directory exists and is writable
RUN mkdir -p /app/bot/cache && chown -R appuser:appgroup /app/bot/cache

USER appuser

ENTRYPOINT ["python", "bot_app.py"]
