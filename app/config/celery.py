# This module sets up the Celery application and its configuration.

# Modules:
#     logging: Provides logging capabilities.
#     celery: Celery framework for distributed task queue.
#     app.config.celery_config: Celery configuration settings.
#     app.config.config: Application configuration settings.
#     app.config.structlog: Structured logging setup.
#     .celery_dlq: Dead-letter queue setup for Celery.

# Functions:
#     on_after_setup_logger(**kwargs): Configures the startup event of Celery to disable Celery logs in production.

# Attributes:
#     logger: Structured logger for the module.
#     celery_app: Configured Celery application instance.
import logging

from celery import Celery
from celery.signals import setup_logging

import app.config.celery_config as celery_config
from app.config.config import get_settings
from app.config.structlog import get_struct_logger

from .celery_dlq import setup_default_dlq

logger = get_struct_logger(__name__)

celery_app = Celery()
celery_app.config_from_object(celery_config)
celery_app.conf.update(
    consumer_timeout=31622400000,
    timezone="America/Sao_Paulo",
    enable_utc=True,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    worker_max_tasks_per_child=1000,
    worker_cancel_long_running_tasks_on_connection_loss=True,
)
celery_app.autodiscover_tasks()
setup_default_dlq(celery_app)


@setup_logging.connect
def on_after_setup_logger(**kwargs):  # pylint: disable=unused-argument
    """Configure startup event of celery.

    Args:
    -   **kwargs: Arguments of celery startup event

    """
    if "production" not in get_settings().app_env.lower():
        return

    # FIX-ME: This code disables logs from celery in production.
    # Application logs are shown as JSON, but celery internal logs are not
    for logger_name in logging.root.manager.loggerDict:
        if logger_name.startswith("celery"):
            logger.debug(f"Deactivate celery logging -> {logger_name}")
            celery_logger = logging.getLogger(logger_name)
            celery_logger.propagate = False
            celery_logger.handlers = []
