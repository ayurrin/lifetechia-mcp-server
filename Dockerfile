FROM python:3.12-slim-bookworm

WORKDIR /app

COPY MCP_financial_data/pyproject.toml ./
COPY MCP_financial_data/lifetechia.py ./
COPY MCP_financial_data/README.md ./

RUN pip install uv
RUN uv venv
RUN . .venv/bin/activate
RUN uv add "mcp[cli]" httpx

CMD ["uv", "run", "lifetechia.py"]
