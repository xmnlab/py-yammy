from dataclasses import dataclass


@dataclass
class MockEventKey:
    type: str = ""
    key: str = ""


@dataclass
class MockSprite:
    attributes = {
        "pos_x": 0,
        "pos_y": 0,
    }

    def attr_update(self, attr, i):
        self.attributes[attr] += i


class MockYammy:
    def __init__(self, events):
        self.events = events

    def get_events(self):
        return self.events
