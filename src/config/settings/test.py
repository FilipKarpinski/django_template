from config.settings.base import *  # noqa: F403
from config.settings.base import env

# configure db name for testing
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://djangouser:djangopw@db:5432/djangodb_test",
    ),
}
