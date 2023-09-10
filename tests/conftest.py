import pytest
from fastapi.testclient import TestClient

from sandfly.app import app


@pytest.fixture
def client():
    return TestClient(app)
