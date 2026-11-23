
import pygame
import logging


def apply_deadzone(value, deadzone):
    if abs(value) < deadzone:
        return 0.0

    return value


class JoystickManager:

    def __init__(self, deadzone=0.10, axis_mapping=None):
        self.deadzone = deadzone
        self.axis_mapping = axis_mapping or {
            "horizontal": 0,
            "vertical": 1
        }

        self.joysticks = {}
        self.logger = logging.getLogger(__name__)

    def initialize(self):
        pygame.init()
        pygame.joystick.init()

        self.logger.info("Joystick system initialized")

        for index in range(pygame.joystick.get_count()):
            self._add_device(index)

    def _add_device(self, device_index):
        try:
            joystick = pygame.joystick.Joystick(device_index)

            if not joystick.get_init():
                joystick.init()

            instance_id = joystick.get_instance_id()

            if instance_id in self.joysticks:
                return

            self.joysticks[instance_id] = joystick

            self.logger.info(
                "Controller connected: %s | ID: %s | GUID: %s",
                joystick.get_name(),
                instance_id,
                joystick.get_guid()
            )

        except pygame.error as error:
            self.logger.error(
                "Could not initialize controller: %s", error
            )

    def _remove_device(self, instance_id):
        joystick = self.joysticks.pop(instance_id, None)

        if joystick is not None:
            name = joystick.get_name()
            joystick.quit()

            self.logger.warning(
                "Controller disconnected: %s", name
            )

    def get_axis_value(self, joystick, axis_index):
        if axis_index < joystick.get_numaxes():
            value = joystick.get_axis(axis_index)

            return apply_deadzone(
                value,
                self.deadzone
            )

        return None

    def poll(self):
        events = pygame.event.get()

        for event in events:

            if event.type == pygame.JOYDEVICEADDED:
                self._add_device(event.device_index)

            elif event.type == pygame.JOYDEVICEREMOVED:
                self._remove_device(event.instance_id)

        states = {}

        for instance_id, joystick in list(
            self.joysticks.items()
        ):

            if not joystick.get_init():
                continue

            axes = [
                self.get_axis_value(joystick, i)
                for i in range(joystick.get_numaxes())
            ]

            mapped_axes = {}

            for name, index in self.axis_mapping.items():
                mapped_axes[name] = self.get_axis_value(
                    joystick, index
                )

            buttons = [
                bool(joystick.get_button(i))
                for i in range(joystick.get_numbuttons())
            ]

            hats = [
                joystick.get_hat(i)
                for i in range(joystick.get_numhats())
            ]

            states[instance_id] = {
                "name": joystick.get_name(),
                "guid": joystick.get_guid(),
                "axes": axes,
                "mapped_axes": mapped_axes,
                "buttons": buttons,
                "hats": hats
            }

        return states

    def shutdown(self):
        for joystick in list(self.joysticks.values()):
            joystick.quit()

        self.joysticks.clear()

        pygame.quit()

        self.logger.info("Joystick system stopped")
