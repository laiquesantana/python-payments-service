from time import time

from app.config.celery import celery_app
from app.config.config import get_settings
from app.config.structlog import get_struct_logger

logger = get_struct_logger(__name__)


def publish_message(
    message_data: dict,
    broker_topic: str,
    exchange_name: str = "",
) -> dict:
    """Function to publish message.

    Args:
    -   message_data (dict): Message data to publish
    -   broker_topic (str): Broker topic to publish message
    -   exchange_name (str): Exchange name to publish message
    -   app_env (str): APP_ENV. defaults come from config settings

    Returns:
    -   dict: Dictionary with file information

    """
    if exchange_name == "":
        exchange_name = get_settings().rabbit_default_exchange

    try:
        with celery_app.producer_pool.acquire(block=True) as producer:  # type: ignore
            # FIX-ME: this publish should be async
            producer.publish(
                body=message_data,
                routing_key=broker_topic,
                exchange=exchange_name,
                retry=False,
            )
        message_id = message_data.get("event_id", time())
        logger.info(
            f"Published message {message_id} of topic "
            f"{broker_topic} from exchange {exchange_name}"
        )
        return message_data

    except Exception as ex:  # pylint: disable=broad-except
        message = f"Unexpected error on publish message: {ex}."
        logger.critical(message, exc_info=True, stack_info=True)
        raise ex
