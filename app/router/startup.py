import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.config import get_settings
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


@asynccontextmanager
async def config_lifespan(_: FastAPI):
    """Lifespan startup event."""
    app_name = get_settings().app_name
    logger.info(f"{app_name} - Starting server !!!")
    log_config()
    yield
    logger.info(f"{app_name} - Stopping  server...")


def log_config():  # pragma: no cover
    """Configure startup event."""

    # Disable uvicorn logging
    uv_logger = logging.getLogger("uvicorn")
    uv_logger.handlers = []

    uva_logger = logging.getLogger("uvicorn.access")
    uva_logger.handlers = []
