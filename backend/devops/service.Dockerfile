FROM python:3.11
ENV TZ="America/Bogota"
WORKDIR /tfmunir

RUN pip install poetry
COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

RUN apt-get update && apt-get install -y locales && \
    echo "es_ES.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen && \
    update-locale LANG=es_ES.UTF-8

ENV LANG es_ES.UTF-8

COPY . /tfmunir
WORKDIR /tfmunir
EXPOSE 80