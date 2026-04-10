# Django Project

> Claude Code configuration for Django projects with HTMX and modern Python tooling.

## Quick Facts

- **Stack**: Django, PostgreSQL, HTMX
- **Package Manager**: uv
- **Test Command**: `uv run pytest`
- **Lint Command**: `uv run ruff check .`
- **Format Command**: `uv run ruff format .`
- **Type Check**: `uv run ty check`

## Key Directories

- `src/` - Django source root (working directory in Docker)
- `src/apps/` - Django applications
- `src/config/` - Django settings (base/dev/prod/test), URLs, ASGI/WSGI
- `src/config/settings/` - Split settings by environment
- `templates/` - Django/Jinja2 templates (inside each app)
- `static/` - CSS, JavaScript, images
- `tasks/` - Celery tasks

## Code Style

- Python 3.13+ with type hints required
- Ruff for linting and formatting (replaces black, isort, flake8)
- ty for type checking (Astral's type checker)
- No `Any` types - use proper type hints or `object`
- Use early returns, avoid nested conditionals
- Prefer composition over inheritance

## Git Conventions

- **Branch naming**: `{initials}/{description}` (e.g., `jd/fix-login`)
- **Commit format**: Conventional Commits (`feat:`, `fix:`, `docs:`, etc.)
- **PR titles**: Same as commit format

## Critical Rules

### Error Handling
- NEVER swallow errors silently
- Always show user feedback for errors (Django messages, HTMX response headers)
- Log errors with proper context for debugging

### Views
- Prefer Function-Based Views
- Always validate request.method explicitly
- Return proper HTTP status codes
- Use `select_related()` / `prefetch_related()` to avoid N+1 queries

### Templates & HTMX
- Use template inheritance (`{% extends %}`, `{% block %}`)
- Create partial templates for HTMX responses (`_partial.html` naming)
- Always include `hx-indicator` for loading states
- Handle `HX-Request` header for partial vs full page responses

### Forms
- Use ModelForm for model-backed forms
- Validate in `clean()` and `clean_<field>()` methods
- Always handle form errors in templates
- Disable submit buttons during HTMX requests

### Celery Tasks
- Tasks must be idempotent
- Use proper retry strategies with exponential backoff
- Always log task start/completion/failure
- Pass serializable arguments only (no model instances)

## Testing

- Write failing test first (TDD)
- Use Factory Boy: `UserFactory.create(is_admin=True)`
- Use pytest fixtures in `conftest.py`
- Test behavior, not implementation
- Run tests before committing

## Skill Activation

Before implementing ANY task, check if relevant skills apply:

- Debugging issues → `systematic-debugging` skill
- Exploring Django project (models, URLs, settings) → `django-extensions` skill
- Working with Django models → `django-models` skill
- Working with Django forms → `django-forms` skill
- Working with Django templates → `django-templates` skill
- Working with HTMX patterns → `htmx-patterns` skill
- Working with Celery tasks → `celery-patterns` skill
- Writing tests → `pytest-django-patterns` skill
- Creating new skills → `skill-creator` skill
- Starting a new task → `onboard` skill
- Working a ticket → `ticket` skill
- Reviewing a PR → `pr-review` skill
- Summarizing branch changes → `pr-summary` skill
- Running quality checks → `code-quality` skill
- Checking docs accuracy → `docs-sync` skill
- Committing worktree changes and merging to master/main → `worktree-commit-merge` skill

## Common Commands

```bash
# Just recipes (primary workflow)
just bootstrap                        # Initial setup: env, build, migrate
just start                            # Start app + infra (watch mode)
just stop                             # Stop all services
just test                             # Run tests in Docker
just test-cov                         # Run tests with coverage
just manage migrate                   # Run Django management commands
just manage makemigrations            # Create migrations
just manage createsuperuser           # Create admin user
just ruff                             # Lint and format
just pre                              # Run all pre-commit hooks
just clean                            # Remove cache files

# Local (outside Docker)
uv run ruff check src                 # Lint code
uv run ruff format src                # Format code
uv run ty check                       # Type check

# Django (inside Docker via just)
just manage shell_plus                # Enhanced shell (django-extensions)

# Celery
uv run celery -A config worker -l info
uv run celery -A config beat -l info

# Dependencies
uv sync                               # Install from pyproject.toml
uv add <package>                      # Add new dependency
uv add --dev <package>                # Add dev dependency

# Git
gh pr create                          # Create PR
```