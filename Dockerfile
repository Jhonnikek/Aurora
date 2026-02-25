FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /uvx /bin/

WORKDIR /bot

COPY . /bot

RUN uv sync --locked

CMD [ "uv", "run", "bot.py" ]
