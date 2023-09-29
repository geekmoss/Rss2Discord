FROM python:3.11-alpine

ENV APP_DIR /app
ENV PYTHONPATH ${APP_DIR}

RUN mkdir $APP_DIR
WORKDIR ${APP_DIR}

RUN pip install 'poetry'

COPY ./pyproject.toml ./poetry.lock ${APP_DIR}/

RUN poetry config virtualenvs.create false \
    && poetry install --only main --no-interaction --no-ansi

COPY . $APP_DIR/

CMD ["python", "main.py"]