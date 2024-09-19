from fastapi import FastAPI, Security
from pydantic import ValidationError
from uvicorn.protocols.utils import ClientDisconnected

from app.config.structlog import get_struct_logger
from app.controllers.core import core_routes
from app.controllers.v1 import routes_v1
from app.security import verify_api_key

from .handler_exception import (
    handler_client_disconnected,
    handler_exception,
    handler_validation_error,
)

logger = get_struct_logger(__name__)


def config_routes(app: FastAPI) -> FastAPI:
    """Config routes from APP:

    Args:
    -   app(`FastApi`): Instance of app

    Return:
    -   app(`FastApi`): Instance of app with routers

    """
    # Include core routes
    for route in core_routes:
        app.include_router(
            route,
            prefix="/core",
        )

    # Include v1 routes
    for route in routes_v1:
        app.include_router(
            route,
            dependencies=[
                Security(verify_api_key),
            ],
        )
    return app


def config_handler_exceptions(app: FastAPI):
    """Config handler exceptions from APP:

    Args:
    -   app(`FastApi`): Instance of app

    Return:
    -   app(`FastApi`): Instance of app with handlers

    """
    app.add_exception_handler(Exception, handler_exception)
    app.add_exception_handler(ClientDisconnected, handler_client_disconnected)
    app.add_exception_handler(ValidationError, handler_validation_error)
    return app
