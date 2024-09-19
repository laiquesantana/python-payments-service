# celery_consumer.py
# from: https://ahiravan.dev/blog/embracing-celery-part-1-extending/

import logging

from celery import Task, bootsteps, shared_task
from kombu import Consumer

from app.config.celery import celery_app as current_app
from app.config.celery_dlq import setup_dlq
from app.config.config import get_settings

_registry = {}

logger = logging.getLogger(__name__)


def _custom_consumer_factory(queue, callback, kwargs):
    class BaseCustomConsumer(bootsteps.ConsumerStep):
        requires = (
            "celery.worker.consumer:Connection",
            "celery.worker.consumer.tasks:Tasks",
        )

        def start(self, parent):
            logger.info(
                f"Consuming from {queue.name} key={queue.routing_key}, exchange={queue.exchange}"
            )
            return super().start(parent)

        def handle_message(self, body, message):
            callback.delay(body)
            message.ack()

        def on_decode_error(self, message, exc):
            message.reject()

        def get_consumers(self, channel):
            options = {"accept": ["json"]}
            consumer_options = kwargs.pop("consumer_options", {})
            options.update(consumer_options)
            return [
                Consumer(
                    channel,
                    queues=[queue],
                    callbacks=[self.handle_message],
                    on_decode_error=self.on_decode_error,
                    **options,
                )
            ]

    return type(f"{queue.name}Consumer", (BaseCustomConsumer,), {})


def _make_consumer(func, **kwargs):
    from kombu import Exchange, Queue

    queue = kwargs.pop("queue", None)
    routing_key = kwargs.pop("routing_key", None)

    if not queue:
        raise RuntimeError("queue is a required parameter for consume_from")

    should_setup_dlq = bool(kwargs.get("setup_dlq", True))
    if isinstance(queue, Queue):
        queue_obj = queue
    else:
        if not routing_key:
            raise RuntimeError("routing_key is required when passing Queue as string")

        _qoptions = {"no_declare": not should_setup_dlq}
        queue_options = kwargs.pop("queue_options", {})
        _qoptions.update(queue_options)

        if "exchange" not in _qoptions:
            default_exchange_name = get_settings().rabbit_default_exchange
            _qoptions["exchange"] = Exchange(default_exchange_name, type="topic")

        _qoptions["routing_key"] = routing_key
        queue_obj = Queue(queue, **_qoptions)

        if should_setup_dlq:
            setup_dlq(current_app, queue_obj)

    return _custom_consumer_factory(queue_obj, func, kwargs), queue_obj


def consume_from(*args, **kwargs):
    """
    :param args: empty. will resolve to the wrapped function
    :param kwargs: queue - either string or kombu.Queue Instance, and other kwargs of kombu.Queue
    :return: the wrapped function

    Usage
    -----

    a)
    @consume_from(queue='<queue_name>', routing_key='<rk>')
    def process_message(body, message):
        pass


    b)
    exchange = Exchange("example", "topic")
    queue = Queue("example", exchange, routing_key="com.example")

    @consume_from(queue=queue)
    def process_message(body, message):
        pass

    """

    def decorator(**options):
        def __inner(func):
            consumer, queue = _make_consumer(func, **options)

            if queue.name in _registry:
                raise RuntimeError(
                    f"Already registered {_registry[queue.name]} for {queue.name}"
                )
            logger.info(
                f"Registering: {func} for queue {queue.name} and routing key {queue.routing_key}"
            )
            _registry[queue.name] = func
            current_app.steps["consumer"].add(consumer)

            if not isinstance(func, Task):
                return shared_task(func)
            return func

        return __inner

    if len(args) == 1 and callable(args[0]):
        return decorator(**kwargs)(args[0])
    return decorator(*args, **kwargs)
