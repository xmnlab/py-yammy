"""Test basic functions."""
from yammy.input import (
    KEY_ARROW_DOWN,
    KEY_ARROW_LEFT,
    KEY_ARROW_RIGHT,
    KEY_ARROW_UP,
    TYPE_KEYDOWN,
    Keyboard,
)

from .utils import MockEventKey, MockSprite, MockYammy


def test_keyboard():

    mock_sprite = MockSprite()

    event_map = {
        "ARROW-UP": lambda sprite: sprite.update("pos_y", -1),
        "ARROW-DOWN": lambda sprite: sprite.update("pos_y", +1),
        "ARROW-LEFT": lambda sprite: sprite.update("pos_x", -1),
        "ARROW-RIGHT": lambda sprite: sprite.update("pos_x", +1),
    }
    keyboard = Keyboard(mock_sprite, event_map)

    game = MockYammy(
        [
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_UP),
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_UP),
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_LEFT),
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_LEFT),
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_DOWN),
            MockEventKey(TYPE_KEYDOWN, KEY_ARROW_RIGHT),
        ]
    )

    keyboard.events("", game)

    assert mock_sprite.attributes["pos_x"] == -1
    assert mock_sprite.attributes["pos_y"] == -1
