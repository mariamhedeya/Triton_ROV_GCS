def apply_deadzone(value, deadzone):
    if abs(value) < deadzone:
        return 0.0

    return value