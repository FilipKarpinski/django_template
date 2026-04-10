# django-docker-starter

An opinionated boilerplate project using Django with a dockerized development environment and a production-ready docker image for deployment.

- Django 5.1
- Python 3.13
- Postgres 17
- Docker Compose for local development
- Dockerfile for building a production-ready image
- Justfile recipes
- uv for package and project management
- ruff, pytest, django-environ, and many more nice tools


## Get Started
This project leverages [uv](https://docs.astral.sh/uv/getting-started/installation/), [just](https://github.com/casey/just) and [Docker Compose](https://docs.docker.com/compose/install/) for managing the development environment. Make sure you have installed he necessary dependencies for running them on your local machine.

Initialize the dev environment with the `just bootstrap` recipe. This will build the dev image and prepare everything before you can start the app and the dependant infrastructure services with the `just start` recipe. Stop all services with hitting `CTRL+C` or using the `just stop` recipe in another terminal. 

```sh
just bootstrap
just start
```

## Usage
The most used project commands are available as just recipe:
```shell
just [recipe]
```

```make
Available recipes:
    bootstrap *ARGS   # bootstrap project
    build *ARGS       # build project
    start *ARGS       # start project
    stop *ARGS        # stop project
    infra-start *ARGS # start infra services
    infra-stop *ARGS  # stop infra services
    app-start *ARGS   # start django app
    app-stop *ARGS    # start django app
    run *ARGS         # uv run command in container
    manage *ARGS      # run django management command
    env               # copy .env.example to .env if not exists
    pre *ARGS         # run pre-commit processes
    ruff *ARGS        # run ruff linting & formatting
    test *ARGS        # run tests
    test-cov *ARGS    # run tests with coverage
    clean *ARGS       # clean up cache files etc.
    prod-start *ARGS  # start production stack
    prod-stop *ARGS   # stop production stack
```


## Prerequisites

### Local Development

- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager
- [just](https://github.com/casey/just) - Command runner
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

Copy `.env.example` to `.env` (done automatically by `just bootstrap`). The defaults work out of the box for local development.

### CI/CD

The GitHub Actions workflow requires no additional secrets for lint and test jobs. The `GITHUB_TOKEN` is provided automatically by GitHub.

On push to `main`, the `release` job builds a Docker image and pushes it to GitHub Container Registry (`ghcr.io`). For this to work:

1. **Enable write access for GitHub Actions** — go to Settings > Actions > General > Workflow permissions and set to **"Read and write permissions"**
2. No extra secrets needed — `GITHUB_TOKEN` has `packages: write` permission configured in the workflow

The image is published as `ghcr.io/<owner>/<repo>:latest` and `ghcr.io/<owner>/<repo>:sha-<commit>`.

### Production Deployment

1. Copy `.env.prod.example` to `.env` on your production server
2. Fill in the required values:
   - `DJANGO_SECRET_KEY` — generate with `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`
   - `DJANGO_ALLOWED_HOSTS` — comma-separated list of your domain(s)
   - `POSTGRES_PASSWORD` — strong database password
   - `DATABASE_URL` — must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`
   - `APP_IMAGE` — your ghcr.io image (e.g., `ghcr.io/<owner>/<repo>:latest`)
3. Start with `just prod-start` or `docker compose -f compose.prod.yml up -d`