FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/.venv/bin:$PATH"

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project --extra api

COPY api/ api

# ENVs needed to be provided on run-time:
# POSTGRES_HOST
# POSTGRES_PORT
# POSTGRES_USER
# POSTGRES_PASSWORD

CMD ["uvicorn", "--host", "0.0.0.0", "api.country_data_api:app"]
