from fastapi import FastAPI

# This module initializes and configures a FastAPI application.

# Imports:
# - FastAPI: The main class for creating a FastAPI application.
# - get_settings: Function to retrieve application settings.
# - get_struct_logger: Function to get a structured logger.
# - config_middleware: Function to configure middlewares.
# - config_handler_exceptions: Function to configure exception handlers.
# - config_lifespan: Function to configure the lifespan of the application.
# - config_routes: Function to configure application routes.

# Functions:
# - init_app: Initializes and configures the FastAPI application.

# Variables:
# - logger: Structured logger instance.
# - app: Initialized FastAPI application instance.

# Function `init_app`:
# - Initializes a FastAPI application with specific settings and configurations.
# - Sets the root path and server URL from the application settings.
# - Sets the application title to "Fastapi Base".
# - Disables the default documentation URLs (docs, openapi, redoc).
# - Configures the lifespan, routes, exception handlers, and middlewares for the application.
# - Returns the configured FastAPI application instance.

from app.config.config import get_settings
from app.config.structlog import get_struct_logger
from app.middlewares import config_middleware
from app.router import config_handler_exceptions, config_lifespan, config_routes

logger = get_struct_logger(__name__)


def init_app() -> FastAPI:
    """Initialize FastAPI application.

    Return:
    -   app(`FastAPI`): Initialized FastAPI application

    """
    _app = FastAPI(
        root_path=get_settings().prefix_url_path,
        servers=[
            {
                "url": get_settings().prefix_url_path,
            }
        ],
        title="Fastapi Base",
        docs_url=None,
        openapi_url=None,
        redoc_url=None,
        lifespan=config_lifespan,
    )
    _app = config_routes(_app)
    _app = config_handler_exceptions(_app)
    _app = config_middleware(_app)
    return _app


app = init_app()
