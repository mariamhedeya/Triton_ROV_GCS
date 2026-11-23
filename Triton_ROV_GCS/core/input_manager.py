
import threading
import time
import logging

from input_devices.joystick import JoystickManager
from input_devices.keyboard import KeyboardManager


class InputManager:

    def __init__(
        self,
        event_bus,
        polling_rate=50,
        deadzone=0.10,
        axis_mapping=None
    ):

        self.event_bus = event_bus
        self.polling_rate = polling_rate
        self.deadzone = deadzone
        self.axis_mapping = axis_mapping

        self.keyboard = KeyboardManager()

        self.running = threading.Event()
        self.thread = None

        self.logger = logging.getLogger(__name__)

    def start(self):

        if self.running.is_set():
            return

        self.keyboard.start()
        self.running.set()

        self.thread = threading.Thread(
            target=self._input_loop,
            name="ROV-Input-Thread",
            daemon=True
        )

        self.thread.start()

        self.logger.info("Input manager started")

    def _input_loop(self):

        joystick = JoystickManager(
            deadzone=self.deadzone,
            axis_mapping=self.axis_mapping
        )

        try:
            joystick.initialize()

            interval = 1.0 / self.polling_rate
            next_tick = time.perf_counter()

            while self.running.is_set():

                controllers = joystick.poll()

                keyboard_state = self.keyboard.get_state()

                input_data = {
                    "controllers": controllers,
                    "keyboard": keyboard_state,
                    "timestamp": time.time()
                }

                self.event_bus.publish(
                    "input_update",
                    input_data
                )

                next_tick += interval

                sleep_time = (
                    next_tick - time.perf_counter()
                )

                if sleep_time > 0:
                    self.running.wait(sleep_time)
                else:
                    next_tick = time.perf_counter()

        except Exception:
            self.logger.exception("Input thread failed")

        finally:
            joystick.shutdown()

    def stop(self):

        self.running.clear()

        self.keyboard.stop()

        if self.thread:
            self.thread.join(timeout=5)

            if self.thread.is_alive():
                self.logger.error(
                    "Input thread did not stop in time"
                )

        self.logger.info("Input manager stopped")
