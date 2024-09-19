import asyncio
from threading import Thread

EVENT_LOOP_THREAD = None


def start_background_loop(loop) -> None:
    loop.run_forever()


def ensure_event_loop_is_running():
    global EVENT_LOOP_THREAD  # pylint: disable=W0603
    if not EVENT_LOOP_THREAD:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        EVENT_LOOP_THREAD = Thread(
            target=start_background_loop,
            args=(loop,),
            daemon=True,
        )

    if not EVENT_LOOP_THREAD.is_alive():
        EVENT_LOOP_THREAD.start()

    return asyncio.get_event_loop()
