from typing import Callable

from fastapi import FastAPI, Request
from starlette.background import BackgroundTask

from app.config.structlog import get_struct_logger, request_formatter

logger = get_struct_logger(__name__)


def config_middleware(app: FastAPI):
    """Config middleware from APP:

    Args:
    -   app(`FastApi`): Instance of app
    -   logger(`BoundLogger`): Logger instance

    Return:
    -   app(`FastApi`): Instance of App with middlewares

    """
    app.middleware("http")(log_request)
    return app


async def log_request(request: Request, call_next: Callable):
    """Configure logging for each request.

    Args:
    -   request(`Request`): Request object
    -   call_next(`Callable`): Next function to be called

    Return:
        Response: Response object

    """
    response = await call_next(request)
    response.background = BackgroundTask(request_formatter, logger, request, response)
    return response
