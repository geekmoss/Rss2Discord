FROM ghcr.io/astral-sh/uv:python3.12-alpine

ENV APP_DIR=/app
ENV PYTHONPATH=${APP_DIR}

RUN mkdir ${APP_DIR}
WORKDIR ${APP_DIR}

COPY ./pyproject.toml ${APP_DIR}/
COPY ./uv.lock ${APP_DIR}/

RUN uv sync --frozen

COPY . ${APP_DIR}/

CMD [ "uv", "run", "main.py" ]
