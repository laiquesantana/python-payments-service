# This module provides security utilities for FastAPI, including API key verification and basic authentication.

# Functions:
#     verify_api_key(api_key_header: str) -> bool:
#         Verifies the provided API key against the expected API key from settings.
#             api_key_header (str): The API key provided in the request header.
#             HTTPException: If the API key is incorrect or missing.
#         Returns:
#             bool: True if the API key is correct.

#     verify_basic_auth(credentials: HTTPBasicCredentials) -> str:
#         Verifies the provided basic authentication credentials against the expected credentials from settings.
#             credentials (HTTPBasicCredentials): The basic authentication credentials provided in the request.
#             HTTPException: If the username or password is incorrect.
#         Returns:
#             str: The username if the credentials are correct.
import secrets


from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security.api_key import APIKeyHeader

from app.config.config import get_settings
from app.config.structlog import get_struct_logger

api_key_header_auth = APIKeyHeader(
    name="X-API-KEY",
    description="Mandatory API Token, required for all endpoints",
    auto_error=True,
)
basic_auth_http = HTTPBasic()
logger = get_struct_logger(__name__)


async def verify_api_key(api_key_header: str = Security(api_key_header_auth)):
    """Function to verify the API key.

    Args:
        api_key_header (str): API key header

    Raises:
        HTTPException: If the API key is wrong or missing

    """
    api_key = get_settings().api_key
    correct_api_key = secrets.compare_digest(api_key_header, api_key)
    if not correct_api_key:
        message = "Wrong or missing API key"
        logger.exception(message, exc_info=True, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=message,
        )
    return True


def verify_basic_auth(credentials: HTTPBasicCredentials = Depends(basic_auth_http)):
    """Function to verify the basic authentication.

    Args:
        credentials (HTTPBasicCredentials): Basic authentication credentials

    Raises:
        HTTPException: If the credentials are wrong

    """
    settings = get_settings()
    is_correct_username = secrets.compare_digest(
        credentials.username, settings.username_docs
    )
    is_correct_password = secrets.compare_digest(
        credentials.password, settings.password_docs
    )
    if not (is_correct_username and is_correct_password):
        message = "Incorrect username or password"
        logger.exception(message, exc_info=True, stack_info=True)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username
