
from queue import Queue, Empty
import logging


class EventBus:

    def __init__(self):
        self.subscribers = {}
        self.queue = Queue()
        self.logger = logging.getLogger(__name__)

    def subscribe(self, event_type, callback):
        self.subscribers.setdefault(
            event_type, []
        ).append(callback)

    def publish(self, event_type, data=None):
        self.queue.put((event_type, data))

    def process_events(self, max_events=100):

        processed = 0

        while processed < max_events:

            try:
                event_type, data = self.queue.get_nowait()

            except Empty:
                break

            try:
                callbacks = self.subscribers.get(
                    event_type, []
                )

                for callback in callbacks:
                    try:
                        callback(data)

                    except Exception:
                        self.logger.exception(
                            "Event callback failed: %s",
                            event_type
                        )

            finally:
                self.queue.task_done()

            processed += 1

        return processed
