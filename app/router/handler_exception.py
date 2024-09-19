from fastapi import status
from fastapi.responses import JSONResponse

from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


async def handler_validation_error(request, ex):  # pragma: no cover
    """Exception handler to ValidationError exception.

    Args:
    -   request: Request to handler
    -   ex: Raised exception

    Return:
    -   JSONResponse: Formatted responde on handler ValidationError exception

    """
    message = "Validation error on receive request."
    logger.error(
        message,
        extra_info={
            "exception": ex,
            "request": request,
        },
        exc_info=True,
        stack_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": ex.errors()},
    )


async def handler_client_disconnected(request, ex):  # pragma: no cover
    """Exception handler to ClientDisconnected exception.

    Args:
    -   request: Request to handler
    -   ex: Raised exception

    Return:
    -   JSONResponse: Formatted responde on handler ClientDisconnected exception

    """
    message = "Client Disconnected error on receive request."
    logger.error(
        message,
        extra_info={
            "exception": ex,
            "request": request,
        },
        exc_info=True,
        stack_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": ex.errors()},
    )


async def handler_exception(request, ex):  # pragma: no cover
    """Exception handler to generically exception.

    Args:
    -   request: Request to handler
    -   ex: Raised exception

    Return:
    -   JSONResponse: Formatted responde on handler generically exception

    """
    message = "Unexpected error, see logs for more details."
    logger.critical(
        message,
        extra_info={
            "exception": ex,
            "request": request,
        },
        exc_info=True,
        stack_info=True,
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": message},
    )
