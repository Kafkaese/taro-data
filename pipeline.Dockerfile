FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.11.26 /uv /uvx /bin/

ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    PATH="/.venv/bin:$PATH"

# Install taro package
COPY pyproject.toml uv.lock ./
COPY taro/ taro
RUN uv sync --locked --no-dev

# CSVs come from S3 at run time (see S3_DATA_BUCKET in pipeline.py) rather
# than being baked into the image here.

# Run pipelines
CMD ["python", "/taro/pipeline.py"]
