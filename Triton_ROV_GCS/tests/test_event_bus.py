
from core.event_bus import EventBus


def test_event_publishing():

    bus = EventBus()

    received = []

    bus.subscribe(
        "test_event",
        lambda data: received.append(data)
    )

    bus.publish("test_event", 123)

    bus.process_events()

    assert received == [123]


def test_multiple_subscribers():

    bus = EventBus()

    received = []

    bus.subscribe("test", lambda data: received.append(data))
    bus.subscribe("test", lambda data: received.append(data * 2))

    bus.publish("test", 5)

    bus.process_events()

    assert received == [5, 10]


def test_unknown_event():

    bus = EventBus()

    bus.publish("unknown", 123)

    assert bus.process_events() == 1
