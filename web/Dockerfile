FROM python:3.8-alpine

RUN apk update && apk upgrade

RUN pip install --no-cache-dir pipenv pip setuptools -U

RUN apk add --no-cache --virtual .build-deps \
    postgresql-dev linux-headers musl-dev \
    ca-certificates gcc

RUN rm -rf /var/cache/apk/*

WORKDIR /code

COPY Pipfile Pipfile.lock ./

RUN mkdir -p .venv && \
    export PIP_NO_CACHE_DIR=false && \
    pipenv install --deploy --dev

COPY . .

RUN export PIP_NO_CACHE_DIR=false && \
    pipenv run pip install -e .

ENTRYPOINT ["pipenv", "run"]

CMD ["gunicorn", "--pythonpath", "src", "-b", "0.0.0.0:8000", "-w", "4", "--reload", "--access-logfile", "-", "--error-logfile", "-", "--log-level", "debug", "main.wsgi"]
