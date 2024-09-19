import logging
import logging.config
import sys
from http import HTTPStatus

import structlog
from fastapi import Request, Response

from app.config.config import get_settings


def configure_struct_logging(level: str):  # pragma: no cover
    """Configure structlog logging.

    Args:
    -   level(`str`) - Level of logger

    """
    # Configure structlog logging
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.CallsiteParameterAdder(
                [
                    structlog.processors.CallsiteParameter.FUNC_NAME,
                    structlog.processors.CallsiteParameter.LINENO,
                ],
            ),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.TimeStamper(fmt="iso", utc=True),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    # Configure logging from stdout
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )


def extra_request_logging(
    request: Request,
    response: Response,
) -> dict:  # pragma: no cover
    """Get extra request info for logging.

    Args:
        request (Request): Request object
        response (Response): Response object

    Returns:
        dict: Extra request info

    """
    status_reasons = {x.value: x.name for x in list(HTTPStatus)}
    return {
        "req": {
            "url": request.url.path,
            "headers": {
                "host": request.headers["host"],
                "user-agent": request.headers["user-agent"],
                "accept": request.headers["accept"],
            },
            "method": request.method,
            "httpVersion": request.scope["http_version"],
            "originalUrl": request.url.path,
            "query": dict(request.query_params),
        },
        "res": {
            "statusCode": response.status_code,
            "body": {
                "statusCode": response.status_code,
                "status": status_reasons.get(response.status_code),
            },
        },
    }


def request_formatter(
    logger: structlog.BoundLogger,
    request: Request,
    response: Response,
) -> None:
    """Log request and response formatter.

    Args:
    -   logger (structlog): Logger object
    -   request (Request): Request object
    -   response (Response): Response object

    """
    try:
        logger.info(
            event=f"{request.method} {request.url.path}",
            extra={"extra_info": extra_request_logging(request, response)},
        )

    except Exception as ex:
        logger.critical(
            ex,
            exc_info=True,
            stack_info=True,
        )
        raise ex


def get_struct_logger(
    name: str,
    level: str = "",
) -> structlog.BoundLogger:  # pragma: no cover
    """Get structlog logger.

    Args:
    -   name (str): Logger name
    -   level(`str`) - Level of logger

    """
    if not level:
        level = get_settings().log_level

    configure_struct_logging(level)
    logger: structlog.BoundLogger = structlog.getLogger(name).bind(name=name)
    return logger
