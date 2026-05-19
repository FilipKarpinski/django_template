from config.settings.base import *  # noqa: F403
from config.settings.base import env

DEBUG = env.bool("DJANGO_DEBUG", default=True)  # type: ignore[arg-type]

ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "0.0.0.0"])  # noqa: S104  # type: ignore[arg-type]

INSTALLED_APPS += ["debug_toolbar"]  # noqa: F405

MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]  # noqa: F405

# required by debug_toolbar; 172.18.0.1 is the Docker bridge gateway (host browser IP inside container)
INTERNAL_IPS = ["127.0.0.1", "172.18.0.1"]
