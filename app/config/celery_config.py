import logging

from app.config.config import Settings, get_settings
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)
configs = get_settings()

broker_connection_retry_on_startup: bool = False
worker_concurrency: int = 10
broker_url: str = configs.rabbit_url
result_backend: str = configs.redis_url
result_backend_transport_options = {
    "global_keyprefix": f"{configs.app_alias}_celery_",
    "retry_policy": {"timeout": 180.0},
    "result_chord_ordered": True,
}
task_default_exchange = configs.rabbit_default_exchange
task_default_exchange_type = "topic"
task_default_queue = configs.rabbit_default_queue
acks_on_failure_or_timeout = False
task_acks_on_failure_or_timeout = False

include = ["app.workers"]
