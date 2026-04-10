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

On every push to `main`, the CI pipeline builds a Docker image, pushes it to GHCR, then SSHs into your VPS to pull and restart the app. Follow these steps to set it up.

#### 1. Provision the VPS

Install Docker and Docker Compose on your server (e.g., Hetzner, DigitalOcean):

```sh
# Install Docker (Ubuntu/Debian)
curl -fsSL https://get.docker.com | sh
```

#### 2. Create a deploy user on the VPS

```sh
# On the VPS
sudo adduser --disabled-password deploy
sudo usermod -aG docker deploy
```

#### 3. Generate an SSH key pair for CI

On your local machine, generate a dedicated key pair (no passphrase):

```sh
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -C "github-actions-deploy" -N ""
```

Add the **public** key to the VPS:

```sh
# Copy the public key to the deploy user's authorized_keys
ssh-copy-id -i ~/.ssh/deploy_key.pub deploy@<your-vps-ip>
```

#### 4. Add GitHub repository secrets

Go to your repo **Settings > Secrets and variables > Actions** and add:

| Secret | Value |
|--------|-------|
| `DEPLOY_HOST` | Your VPS IP address or hostname |
| `DEPLOY_USER` | `deploy` (or whichever user you created) |
| `DEPLOY_SSH_KEY` | Contents of `~/.ssh/deploy_key` (the **private** key) |
| `DEPLOY_PATH` | Absolute path to the project on the VPS (e.g., `/home/deploy/myapp`) |

#### 5. Set up the project on the VPS

```sh
# SSH into the VPS as the deploy user
ssh deploy@<your-vps-ip>

# Create the project directory
mkdir -p ~/myapp && cd ~/myapp

# Copy the production compose file and env
# (from your local machine)
scp compose.prod.yml .env.prod.example deploy@<your-vps-ip>:~/myapp/
scp -r nginx deploy@<your-vps-ip>:~/myapp/

# On the VPS, create and configure .env
cd ~/myapp
cp .env.prod.example .env
```

Edit `.env` and fill in the required values:

- `DJANGO_SECRET_KEY` — generate with `python3 -c "import secrets; print(secrets.token_urlsafe(50))"`
- `DJANGO_ALLOWED_HOSTS` — comma-separated list of your domain(s)
- `CSRF_TRUSTED_ORIGINS` — comma-separated, with `https://` prefix (e.g., `https://yourdomain.com`)
- `POSTGRES_PASSWORD` — strong database password
- `DATABASE_URL` — must match `POSTGRES_USER`, `POSTGRES_PASSWORD`, and `POSTGRES_DB`
- `APP_IMAGE` — your GHCR image (e.g., `ghcr.io/<owner>/<repo>:latest`)

#### 6. First deploy

Start the stack manually the first time to run initial migrations:

```sh
cd ~/myapp
docker compose -f compose.prod.yml pull
docker compose -f compose.prod.yml up -d
docker compose -f compose.prod.yml exec app python manage.py migrate
docker compose -f compose.prod.yml exec app python manage.py createsuperuser
```

#### 7. Verify auto-deploy

Push a commit to `main`. The CI pipeline will:

1. **Lint** — ruff, ty, hadolint
2. **Test** — pytest in Docker
3. **Release** — build and push image to `ghcr.io/<owner>/<repo>:latest`
4. **Deploy** — SSH into VPS, pull the new image, restart containers, prune old images

Monitor the workflow in the **Actions** tab of your repository.