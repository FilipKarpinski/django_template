import pytest
from django.test import Client


@pytest.fixture
def api_client(client: Client) -> Client:
    """Alias for Django test client, ready for customization."""
    return client
