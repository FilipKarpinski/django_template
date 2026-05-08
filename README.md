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
This project leverages [uv](https://docs.astral.sh/uv/getting-started/installation/), [just](https://github.com/casey/just) and [Docker Compose](https://docs.docker.com/compose/install/) for managing the development environment. Make sure you have installed the necessary dependencies for running them on your local machine.

Initialize the dev environment with the `just bootstrap` recipe. This will build the dev image and prepare everything before you can start the app and the dependant infrastructure services with the `just start` recipe. Stop all services with hitting `CTRL+C` or using the `just stop` recipe in another terminal. 

```sh
just bootstrap
just start
```

## Usage

All project commands are available as just recipes. Run `just` to list them:

```sh
just
```


## Prerequisites

### Local Development

- [uv](https://docs.astral.sh/uv/getting-started/installation/) - Python package manager
- [just](https://github.com/casey/just) - Command runner
- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)

Copy `.env.example` to `.env` (done automatically by `just bootstrap`). The defaults work out of the box for local development.

### CI/CD

The pipeline uses three branches with distinct responsibilities:

| Event | Jobs | What happens |
|---|---|---|
| Pull request | `lint` + `test` | Code is linted and tested against a throwaway local build — image is never pushed |
| Merge to `release` | `lint` + `build` | Image is built once and pushed to GHCR as `:sha-<commit>` and `:latest` |
| Merge to `main` | `deploy` | `:latest` image is pulled on the VPS, containers restarted, migrations run |

The image is built **only on merge to `release`**. Merging `release` → `main` is a pure deployment trigger — no rebuild.

Enable write access for GitHub Actions so the `build` job can push to GHCR: go to **Settings > Actions > General > Workflow permissions** and set to **"Read and write permissions"**.

### Production Deployment

Follow these steps to set up the VPS and wire up the CI deploy pipeline.

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

#### 4. Verify auto-deploy

Merge a branch into `release`. The pipeline will lint and build the image. Then merge `release` into `main` — the pipeline will copy deployment files, pull the new image, restart containers, and run migrations.

Once the first deploy completes, create a superuser:

```sh
just prod-createsuperuser
```

Monitor the workflow in the **Actions** tab of your repository.