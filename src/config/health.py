from django.http import HttpRequest, HttpResponse


def health_check(request: HttpRequest) -> HttpResponse:  # noqa: ARG001
    return HttpResponse("ok")
