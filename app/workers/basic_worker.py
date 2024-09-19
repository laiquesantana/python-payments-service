import asyncio

from celery import shared_task

from app.config.structlog import get_struct_logger
from app.workers import consume_from, ensure_event_loop_is_running

logger = get_struct_logger(__name__)


@consume_from(
    queue="fast_api_base.basic_worker",
    routing_key="basic.new_task",
)
@shared_task(
    name="run_basic_worker.",
    autoretry_for=(Exception,),
    retry_backoff=30,
    retry_backoff_max=5 * 60,
    retry_jitter=False,
    max_retries=5,
    retry_kwargs={"max_retries": 5},
)
def perform(body: dict):  # pragma: no cover
    event_loop = ensure_event_loop_is_running()
    task = asyncio.run_coroutine_threadsafe(aperform(body), event_loop)
    task.result()


async def aperform(body: dict):
    """Worker function to handle basic worker.

    Params:
    -   body (dict): Message body from rabbitmq

    """
    logger.info(f"Running worker -> {body}. ")
    logger.info(f"Finish worker -> {body}. ")
