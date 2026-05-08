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
    prod-provision *ARGS      # provision production server with ansible
    prod-start *ARGS          # start production stack
    prod-stop *ARGS           # stop production stack
    prod-createsuperuser      # create superuser on production server
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

On every push to `main`, the CI pipeline builds a Docker image, pushes it to GHCR, then SSHs into your VPS to pull and restart the app. Follow these steps to set it up.

#### 1. Generate an SSH key pair for CI

On your local machine, generate a dedicated key pair (no passphrase):

```sh
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "github-actions-deploy" -N ""
```

#### 2. Provision the VPS with Ansible

The `ansible/` directory contains a playbook that fully sets up the server: Docker, deploy user, firewall, and project directory.

```sh
# Copy example files
cp ansible/vars.example.yml ansible/vars.yml
cp ansible/inventory.example ansible/inventory

# Fill in your server IP in inventory and set ci_public_key in vars.yml
# (use the contents of ~/.ssh/deploy_key.pub)

# Run the playbook (requires Ansible and the community.general + posix collections)
ansible-galaxy collection install community.general ansible.posix
just prod-provision
```

After the playbook completes, edit `{{ deploy_path }}/.env` on the server to fill in your production secrets.

#### 3. Add GitHub repository secrets

Go to your repo **Settings > Secrets and variables > Actions** and add:

| Secret | Value |
|--------|-------|
| `DEPLOY_HOST` | Your VPS IP address or hostname |
| `DEPLOY_USER` | `deploy` (or whichever user you created) |
| `DEPLOY_SSH_KEY` | Contents of `~/.ssh/deploy_key` (the **private** key) |
| `DEPLOY_PATH` | Absolute path set in `ansible/vars.yml` (e.g., `/home/deploy/myapp`) |

> `compose.prod.yml` and `nginx/` are copied automatically by the CI pipeline on every deploy — no manual file copying needed.

Edit `.env` and fill in the required values:

- `DJANGO_SECRET_KEY` — generate with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DJANGO_ALLOWED_HOSTS` — comma-separated list of your domain(s)
- `CSRF_TRUSTED_ORIGINS` — comma-separated, with `https://` prefix (e.g., `https://yourdomain.com`)
- `POSTGRES_PASSWORD` — strong database password
- `DATABASE_URL` — must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`
- `APP_IMAGE` — your GHCR image (e.g., `ghcr.io/<owner>/<repo>:latest`)

#### 6. Verify auto-deploy

Push a commit to `main`. The CI pipeline will:

1. **Lint** — ruff, ty, hadolint
2. **Test** — pytest in Docker
3. **Release** — build and push image to `ghcr.io/<owner>/<repo>:latest`
4. **Deploy** — copy `compose.prod.yml` + `nginx/`, pull the new image, restart containers, run migrations, prune old images

Once the first deploy completes, create a superuser:

```sh
just prod-createsuperuser
```

Monitor the workflow in the **Actions** tab of your repository.