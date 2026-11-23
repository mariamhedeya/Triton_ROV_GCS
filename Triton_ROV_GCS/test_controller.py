import pygame
import time

pygame.init()
pygame.joystick.init()

print("Searching for controllers...")

try:
    while True:
        pygame.event.pump()

        count = pygame.joystick.get_count()

        print(f"\nConnected controllers: {count}")

        for i in range(count):
            controller = pygame.joystick.Joystick(i)

            if not controller.get_init():
                controller.init()

            print("\nController:", controller.get_name())
            print("Axes:", controller.get_numaxes())
            print("Buttons:", controller.get_numbuttons())
            print("Hats:", controller.get_numhats())

            for axis in range(controller.get_numaxes()):
                value = controller.get_axis(axis)
                print(f"Axis {axis}: {value:.2f}")

        time.sleep(1)

except KeyboardInterrupt:
    print("Test stopped.")

finally:
    pygame.quit()