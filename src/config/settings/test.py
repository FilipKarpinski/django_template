from config.settings.base import *  # noqa: F403
from config.settings.base import env

# configure db name for testing
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="postgres://djangouser:djangopw@db:5432/djangodb_test",
    ),
}

# Use fast password hasher for tests
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Use in-memory file storage for tests
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.InMemoryStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}
