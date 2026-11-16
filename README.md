
# OWMP

OWMP (Organization Work Management Platform) is a self-hosted foundation for coordinating organizational work, people, projects, tasks, attendance, communication and documentation.

[![Built with Cookiecutter Django](https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg?logo=cookiecutter)](https://github.com/cookiecutter/cookiecutter-django/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

License: MIT

## Settings

Moved to [settings](https://cookiecutter-django.readthedocs.io/en/latest/1-getting-started/settings.html).

## Basic Commands

### Local setup

Install the locked Python and Node dependencies:

    uv sync
    npm ci

Copy `.env.example` to a local `.env` only when using the local Django settings directly. Docker Compose uses the ignored files under `.envs/.local/`; configure those files locally and never commit them.

To start the local service stack:

    docker compose -f docker-compose.local.yml up --build

Apply migrations from another terminal:

    docker compose -f docker-compose.local.yml run --rm django python manage.py migrate

### Setting Up the Initial Administrator

Public registration is not enabled. To create the initial administrator, use:

      uv run python manage.py createsuperuser

### Type checks

Running type checks with mypy:

    uv run mypy owmp

### Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report:

    uv run coverage run -m pytest
    uv run coverage html
    uv run open htmlcov/index.html

#### Running tests with pytest

    uv run pytest

The default test settings use SQLite for self-contained unit tests. Set `DATABASE_URL` explicitly when running PostgreSQL integration tests.

### Frontend assets

Install Node dependencies with `npm ci`, then build CSS with:

    npm run css:build

### Celery

Celery services are available for asynchronous work.

To run a celery worker:

```bash
cd owmp
uv run celery -A config.celery_app worker -l info
```

Please note: For Celery's import magic to work, it is important _where_ the celery commands are run. If you are in the same folder with _manage.py_, you should be right.

To run [periodic tasks](https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html), you'll need to start the celery beat scheduler service. You can start it as a standalone process:

```bash
cd owmp
uv run celery -A config.celery_app beat
```

or you can embed the beat service inside a worker with the `-B` option (not recommended for production use):

```bash
cd owmp
uv run celery -A config.celery_app worker -B -l info
```

### Email Server

In development, it is often nice to be able to see emails that are being sent from your application. For that reason local SMTP server [Mailpit](https://github.com/axllent/mailpit) with a web interface is available as docker container.

Container mailpit will start automatically when you will run all docker containers.
Please check [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/2-local-development/developing-locally-docker.html) for more details how to start all containers.

With Mailpit running, to view messages that are sent by your application, open your browser and go to `http://127.0.0.1:8025`

## Deployment

The following details how to deploy this application.

### Docker

See detailed [cookiecutter-django Docker documentation](https://cookiecutter-django.readthedocs.io/en/latest/3-deployment/deployment-with-docker.html).
