import logging
import queue
from logging.handlers import QueueHandler, QueueListener


def setup_async_logging(app):
    log_queue = queue.Queue(-1)

    queue_handler = QueueHandler(log_queue)
    queue_handler.setLevel(logging.INFO)
    queue_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    file_handler = logging.FileHandler("taskflow.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG if app.debug else logging.INFO)
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    listener = QueueListener(log_queue, file_handler, console_handler, respect_handler_level=True)
    listener.start()

    app.logger.addHandler(queue_handler)
    app.logger.setLevel(logging.DEBUG if app.debug else logging.INFO)
