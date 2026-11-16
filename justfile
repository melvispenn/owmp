# Local development commands.

default:
    @just --list

css:
    @npm run css:build

css-watch:
    @npm run css:watch

manage +args:
    @uv run python manage.py {{args}}

pytest *args:
    @uv run pytest {{args}}

docker-up:
    @docker compose -f docker-compose.local.yml up --build

docker-migrate:
    @docker compose -f docker-compose.local.yml run --rm django python manage.py migrate
