# from: https://ahiravan.dev/blog/embracing-celery-part-1-extending/
from celery import bootsteps
from kombu import Exchange, Queue


def setup_default_dlq(app, dlq_suffix="dead"):
    queue = Queue(
        app.conf.task_default_queue,
        Exchange(app.conf.task_default_exchange, type="topic"),
        routing_key=app.conf.task_default_routing_key,
    )
    setup_dlq(app, queue, dlq_suffix)
    app.conf.task_queues = (queue,)


def setup_dlq(app, queue: Queue, dql_suffix="dead"):
    deadletter_queue_name = f"{queue.name}.{dql_suffix}"
    deadletter_exchange_name = f"fast_api.{dql_suffix}"
    deadletter_routing_key = "fast_api.dead"

    if queue.queue_arguments is None:
        queue.queue_arguments = {}

    queue.queue_arguments.update(
        {
            "x-dead-letter-exchange": deadletter_exchange_name,
            "x-dead-letter-routing-key": deadletter_routing_key,
        }
    )

    if deadletter_queue_name != "fast_api.dead":
        return

    class DeclareDLXnDLQ(bootsteps.StartStopStep):
        """Celery Bootstep to declare the DL exchange and queues before the worker
        starts processing tasks."""

        requires = {"celery.worker.components:Pool"}

        def start(self, worker):
            dlx = Exchange(deadletter_exchange_name, type="direct")

            dead_letter_queue = Queue(
                deadletter_queue_name, dlx, routing_key=deadletter_routing_key
            )

            with worker.app.pool.acquire() as conn:
                dead_letter_queue.bind(conn).declare()

    app.steps["worker"].add(DeclareDLXnDLQ)
