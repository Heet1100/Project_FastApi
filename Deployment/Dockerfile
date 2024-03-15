FROM python:3.8.2-slim-buster
LABEL authors="heet.mehta_everestek"
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /ben-admin

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    WORKDIR_PATH="/ben-admin" \
    VENV_PATH="/venv"

RUN python -m venv $VENV_PATH
ENV PATH ="$VENV_PATH/bin:$PATH"

RUN pip install --no-cache-dir --compile --upgrade pip poetry

COPY ./pyproject.toml /ben-admin/pyproject.toml

RUN poetry config virtualenvs.create false && poetry install --no-root --no-dev

COPY ./service_version.py /ben-admin/service_version.py
COPY ./deployments/entrypoint.sh /ben-admin/entrypoint.sh
COPY ./main.py /ben-admin/main.py
COPY ./alembic.ini /ben-admin/alembic.ini

COPY ./src /ben-admin/src
COPY ./alembic /ben-admin/alembic

RUN chmod +x /ben-admin/entrypoint.sh

RUN mkdir -p /ben-admin/log

EXPOSE 8001
CMD ["/ben-admin/entrypoint.sh"]
