from http import HTTPStatus

from django.test import Client


def test_demo_index_view(client: Client) -> None:
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert b"<h1>Hello World!</h1>" in response.content


def test_base_template_wires_frontend_assets_and_csrf(client: Client) -> None:
    response = client.get("/")
    body = response.content
    # Vendored assets must load and every htmx request must carry the CSRF token.
    assert b"vendor/tailwind.css" in body
    assert b"vendor/htmx.min.js" in body
    assert b"vendor/alpine.min.js" in body
    assert b"X-CSRFToken" in body
