FROM public.ecr.aws/lambda/python:3.14-arm64

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never

# Lambda's base image expects dependencies + code flat under
# LAMBDA_TASK_ROOT (/var/task), not a venv - `uv sync` (used by
# api.Dockerfile/pipeline.Dockerfile) doesn't fit that layout, so this
# exports the locked dependency set and installs it with --target instead.
# The api/ code doesn't import anything from the taro package itself
# (only api.Dockerfile/pipeline.Dockerfile's targets do), so this only
# needs the "api" extra, not the project itself.
COPY pyproject.toml uv.lock ./
RUN uv export --locked --no-dev --extra api --no-emit-project --format requirements-txt -o requirements.txt \
    && uv pip install --target "${LAMBDA_TASK_ROOT}" -r requirements.txt

COPY api/ "${LAMBDA_TASK_ROOT}/api"

# ENVs needed to be provided at runtime (same as api.Dockerfile):
# ENV, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

CMD ["api.country_data_api.handler"]
