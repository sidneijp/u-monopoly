# u-monopoly

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/d8cfb19775884f3fa5789fe7d5896482)](https://app.codacy.com/manual/sidneijp/u-monopoly?utm_source=github.com&utm_medium=referral&utm_content=sidneijp/u-monopoly&utm_campaign=Badge_Grade_Dashboard)

Micro Monopoly is a simplified "Monopoly" like game.

## Dependencies

- docker >= 19.03
- docker-compose >= 1.25

## Quickstart

Build:

```shell script
docker-compose build
```

Prepare environment:

```shell script
cp .env.sample .env
cp web/.env.sample web/.env
# edit .env and web/.env if necessary 
```

Run:

```shell script
docker-compose up
```

## Running tests

Web:

```shell script
docker-compose run --rm web pytest --cov
```
