from fastapi.testclient import TestClient

from app import main
from app.config.config import get_settings

client = TestClient(main.app)


def test_try_access_docs_without_basic_auth():
    """Test if the docs is accessible without basic auth."""
    response = client.get("/core/docs")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


def test_try_access_docs_with_wrong_username():
    """Test if the docs is accessible with wrong username."""
    response = client.get(
        "/core/docs",
        auth=(
            "wronguser",
            get_settings().password_docs,
        ),
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_try_access_docs_with_wrong_password():
    """Test if the docs is accessible with wrong password."""
    response = client.get(
        "/core/docs",
        auth=(
            get_settings().username_docs,
            "wrongpassword",
        ),
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}


def test_access_docs():
    """Test if the docs is accessible."""
    settings = get_settings()
    response = client.get(
        "/core/docs",
        auth=(settings.username_docs, settings.password_docs),
    )
    assert response.status_code == 200


def test_access_open_api():
    """Test if the openapi.json is accessible."""
    settings = get_settings()
    response = client.get(
        "/core/openapi.json",
        auth=(
            settings.username_docs,
            settings.password_docs,
        ),
    )
    assert response.status_code == 200
    assert response.json()["info"]["title"] == "Testes Fastapi Base"
