# u-monopoly
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
