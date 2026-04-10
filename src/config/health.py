from django.db import connection
from django.http import HttpRequest, HttpResponse


def health_check(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    connection.ensure_connection()
    return HttpResponse("ok")
