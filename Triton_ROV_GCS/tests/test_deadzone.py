
from input_devices.joystick import apply_deadzone


def test_deadzone_ignores_small_values():

    assert apply_deadzone(0.05, 0.10) == 0.0
    assert apply_deadzone(-0.05, 0.10) == 0.0


def test_deadzone_keeps_large_values():

    assert apply_deadzone(0.50, 0.10) == 0.50
    assert apply_deadzone(-0.50, 0.10) == -0.50


def test_deadzone_boundary():

    assert apply_deadzone(0.10, 0.10) == 0.10
