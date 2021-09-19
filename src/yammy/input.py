from typing import Callable, Dict

import pygame

# keys
TYPE_KEYDOWN = pygame.KEYDOWN
KEY_ARROW_UP = pygame.K_UP
KEY_ARROW_DOWN = pygame.K_DOWN
KEY_ARROW_LEFT = pygame.K_LEFT
KEY_ARROW_RIGHT = pygame.K_RIGHT


class Input:
    ...


class Keyboard(Input):

    key_map = {
        KEY_ARROW_LEFT: "ARROW-LEFT",
        KEY_ARROW_RIGHT: "ARROW-RIGHT",
        KEY_ARROW_UP: "ARROW-UP",
        KEY_ARROW_DOWN: "ARROW-DOWN",
    }

    def __init__(self, sprite, callbacks: Dict[str, Callable]):
        self.sprite = sprite
        self.callbacks = callbacks

    def events(self, event, game):
        if event.type == TYPE_KEYDOWN:
            event_map = self.key_map.get(event.key)
            if not event_map:
                return

            callback = self.callbacks.get(event_map)
            if callback:
                callback(self.sprite)
