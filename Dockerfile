# cad-bot: CadQuery-only runtime managed by uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/cad-bot/.venv \
    PYTHONUNBUFFERED=1

WORKDIR /opt/cad-bot

# System libs commonly needed by OCP/CadQuery wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0 \
        libxrender1 \
        libsm6 \
        libxext6 \
        fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock .python-version ./

RUN uv sync --frozen --no-dev

ENV PATH="/opt/cad-bot/.venv/bin:${PATH}" \
    VIRTUAL_ENV=/opt/cad-bot/.venv

WORKDIR /work

CMD ["bash"]
