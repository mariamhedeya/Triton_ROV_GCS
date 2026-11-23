
import time
import logging
from pathlib import Path

from core.config_manager import ConfigManager
from core.event_bus import EventBus
from core.input_manager import InputManager
from utils.logger import setup_logger


def main():

    project_directory = Path(__file__).resolve().parent

    config_manager = ConfigManager(
        project_directory / "config"
    )

    settings = config_manager.load("settings.yaml")
    mappings = config_manager.load("mappings.yaml")

    logging_config = settings["logging"]

    setup_logger(
        level=logging_config["level"],
        log_file=project_directory / logging_config["file"],
        max_bytes=logging_config["max_bytes"],
        backup_count=logging_config["backup_count"]
    )

    logger = logging.getLogger("ROV-GCS")

    logger.info("Starting Triton ROV GCS")

    event_bus = EventBus()

    latest_data = {
        "value": None
    }

    def handle_input(data):
        latest_data["value"] = data

    event_bus.subscribe(
        "input_update",
        handle_input
    )

    input_config = settings["input"]

    axis_mapping = mappings["joystick"]["axes"]

    input_manager = InputManager(
        event_bus=event_bus,
        polling_rate=input_config["polling_rate"],
        deadzone=input_config["deadzone"],
        axis_mapping=axis_mapping
    )

    input_manager.start()

    logger.info("Input system running")

    last_display = 0

    try:

        while True:

            event_bus.process_events()

            current_time = time.monotonic()

            if current_time - last_display >= 0.5:

                data = latest_data["value"]

                if data is not None:

                    print("\n" + "=" * 45)
                    print("       TRITON ROV GROUND CONTROL")
                    print("=" * 45)

                    print("\nKEYBOARD:")

                    for key, value in data["keyboard"].items():
                        print(f"{key}: {value}")

                    print("\nCONNECTED JOY-CONS:")

                    controllers = data["controllers"]

                    if not controllers:
                        print("No controllers detected")

                    for device_id, state in controllers.items():

                        print(f"\nDevice ID: {device_id}")
                        print(f"Name: {state['name']}")
                        print(f"GUID: {state['guid']}")
                        print(f"Axes: {state['axes']}")
                        print(f"Mapped axes: {state['mapped_axes']}")
                        print(f"Buttons: {state['buttons']}")
                        print(f"D-Pad: {state['hats']}")

                last_display = current_time

            time.sleep(0.005)

    except KeyboardInterrupt:

        logger.info("Shutdown requested")

    finally:

        input_manager.stop()

        logger.info("Triton ROV GCS stopped")


if __name__ == "__main__":
    main()
