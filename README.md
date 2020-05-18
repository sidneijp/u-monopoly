# u-monopoly
[![Codacy Badge](https://app.codacy.com/project/badge/Grade/39d03e6d97c7490397f719c1250ef82c)](https://www.codacy.com/manual/sidneijp/u-monopoly?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=sidneijp/u-monopoly&amp;utm_campaign=Badge_Grade)
[![Codacy Badge](https://app.codacy.com/project/badge/Coverage/39d03e6d97c7490397f719c1250ef82c)](https://www.codacy.com/manual/sidneijp/u-monopoly?utm_source=github.com&utm_medium=referral&utm_content=sidneijp/u-monopoly&utm_campaign=Badge_Coverage)
[![CircleCI](https://circleci.com/gh/sidneijp/u-monopoly.svg?style=shield)](https://app.circleci.com/pipelines/github/sidneijp/u-monopoly)

Micro Monopoly is a simplified "Monopoly" like game.

## URLs

- http://locahost:8000/api/ -> root REST API
- http://locahost:8000/api/swagger/ -> Swagger interface
- http://locahost:8000/admin/ -> Django's admin interface
- http://locahost:8000/queue/ -> Redis Queue management interface

## Dependencies

- docker >= 19.03
- docker-compose >= 1.25

## Quickstart

Build container's image:

```shell script
docker-compose build
```

Prepare environment:

```shell script
cp .env.sample .env
cp web/.env.sample web/.env
# edit .env and web/.env if necessary 
```

Run application services:

```shell script
docker-compose up
```

Run database migrations:

```shell script
docker-compose run --rm web src/manage.py migrate
```

Create a superuser:

```shell script
docker-compose run --rm web src/manage.py createsuperuser
```

## Running tests

Run:

```shell script
docker-compose run --rm web pytest --cov
```

Run on "watch mode" (rerun tests when a file changes):

```shell script
docker-compose run --rm web ptw -- --cov
```

## Scale queue workers

```shell script
docker-compose up -d --scale rq=<number of workers> rq
```
