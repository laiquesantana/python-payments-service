import pytest
from fastapi import HTTPException
from fastapi.security import HTTPBasicCredentials

from app.security import verify_api_key, verify_basic_auth
from tests.utils import auth_header


async def test_verify_api_key():
    """Test successfully verify api key."""

    # Arrange
    header = auth_header()
    api_key = header["X-API-KEY"]

    # Act
    is_valid = await verify_api_key(api_key)

    # Assert
    assert is_valid


async def test_verify_api_key_not_found():
    """Test not found verify api key."""

    # Arrange
    message_expected = "Wrong or missing API key"
    api_key = "Randon value"

    # Act
    with pytest.raises(HTTPException) as error:
        await verify_api_key(api_key)

    message_exception = str(error.value)

    # Assert
    assert message_exception in str(message_expected)


async def test_verify_basic_auth():
    """Test successfully verify basic auth."""
    # Arrange
    username = "local"
    password = "local"
    credentials = HTTPBasicCredentials(
        username=username,
        password=password,
    )

    # Act
    name = verify_basic_auth(credentials)

    # Assert
    assert name == username


async def test_verify_basic_auth_invalid():
    """Test invalid verify basic auth."""
    # Arrange
    username = "new user"
    password = "new pass"
    credentials = HTTPBasicCredentials(
        username=username,
        password=password,
    )
    message_expected = "Incorrect username or password"

    # Act
    with pytest.raises(HTTPException) as error:
        await verify_basic_auth(credentials)

    message_exception = str(error.value)

    # Assert
    assert message_exception in str(message_expected)
