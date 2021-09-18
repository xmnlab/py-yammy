from __future__ import annotations

import copy
import glob
from typing import Callable, Dict, List

import pygame
from yammy.input import Keyboard
from yammy.settings import get_path
from yammy.utils import read_config


class SpritesController:
    """
    SpritesController is responsible for controlling sprints.

    It orchestrate the sprites for a specific scene.
    """

    sprites: List[Sprite] = []

    def __init__(self, sprites_instances_config):
        sprites_instances_config = copy.copy(sprites_instances_config)

        if not sprites_instances_config:
            return

        sprites_type = [v["type"] for v in sprites_instances_config]
        sprites_definition = {}
        sprites = []

        # load just the sprites needed
        for f in glob.glob(str(get_path("/sprites") / "*.spr.yaml")):
            sprite = read_config(f)
            if sprite["type"] in sprites_type:
                sprites_definition[sprite["type"]] = sprite

        # create the sprite object
        for sprite in sprites_instances_config:
            sprite.update(sprites_definition[sprite["type"]])
            sprites.append(Sprite(sprite))

        self.sprites = sprites

    def render(self, screen):
        for s in self.sprites:
            s.render(screen)

    def get_events(self):
        events = []
        for s in self.sprites:
            events.extend(s.events)
        return events


class Sprite:
    """
    A specific sprite defined in a spr.yaml file inside the sprites folder.
    """

    config: dict = {}
    events = []
    methods: Dict[str, Callable] = {}
    attributes: Dict[str.Any] = {}

    def __init__(self, config: str):
        self.config = config
        self.load_attributes()
        self.load_methods()
        self.load_events()

    def iattr(self, attr, i):
        self.attributes[attr] += i

    def load_attributes(self):
        self.attributes = {}

        config_attributes = self.config.get("attributes")

        if not config_attributes:
            return

        for m_name, m_attr in config_attributes.items():
            self.attributes[m_name] = m_attr["value"]

    def load_methods(self):
        self.methods = {}

        config_methods = self.config.get("methods")

        if not config_methods:
            return

        for m_name, m_func in config_methods.items():
            self.methods[m_name] = eval(f"lambda sprite: {m_func}")

    def load_events(self):
        self.events = []
        config_events = self.config.get("events")

        if not config_events:
            return

        controllers = config_events.get("controllers", {})

        for controller, events in controllers.items():
            if controller == "keyboard":
                lambda_events = {}

                for k_event, event in events.items():
                    import pdb

                    pdb.set_trace()
                    lambda_events[k_event] = eval(
                        f"lambda sprite: lambda: event, game: {event})"
                    )(self)

                self.events.append(Keyboard(self, lambda_events).events)

    def render(self, screen):
        attributes = self.config["attributes"]
        current = attributes["current"]["value"]
        animation = self.config["animations"][current]
        image = animation["images"][0]

        pos_x = attributes["pos-x"]["value"]
        pos_y = attributes["pos-y"]["value"]

        sprite_filename = str(
            get_path("/assets/sprites") / self.config["type"] / image
        )
        sprite_image = pygame.image.load(sprite_filename).convert()
        screen.blit(sprite_image, [pos_x, pos_y])
        print([pos_x, pos_y])
