
from pynput import keyboard
import threading


class KeyboardManager:

    def __init__(self):
        self.keys = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False
        }

        self.lock = threading.Lock()

        self.mapping = {
            keyboard.Key.up: "forward",
            keyboard.Key.down: "backward",
            keyboard.Key.left: "left",
            keyboard.Key.right: "right"
        }

        self.listener = None

    def start(self):
        if self.listener is not None:
            return

        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )

        self.listener.start()

    def on_press(self, key):
        action = self.mapping.get(key)

        if action:
            with self.lock:
                self.keys[action] = True

    def on_release(self, key):
        action = self.mapping.get(key)

        if action:
            with self.lock:
                self.keys[action] = False

    def get_state(self):
        with self.lock:
            return self.keys.copy()

    def reset(self):
        with self.lock:
            for key in self.keys:
                self.keys[key] = False

    def stop(self):
        self.reset()

        if self.listener and self.listener.is_alive():
            self.listener.stop()
            self.listener.join(timeout=2)

        self.listener = None
