"""Main module template with example functions."""
import io
import base64
from glob import glob
import os
from pathlib import Path
import sys
import time

import pygame
import yaml

from yammy.scene import Scenes
from yammy.utils import read_config
from yammy.settings import get_path


class Yammy:
    config = {}
    clock_tick_rate = 20

    scene = None
    scenes = None
    soundtrack = None
    next_scene_name = None

    screen = None

    def __init__(self, project_path: Path):
        os.environ["PYGE_PROJECT_PATH"] = str(project_path)

        self.config = {}
        self.config["sprites"] = {}

        self.config["main"] = read_config(get_path("/") / "main.yaml")
        self.config["scenes"] = read_config(get_path("/") / "scenes.yaml")

        for f in glob(str(get_path("/sprites") / "*.spr.yaml")):
            _sprite = read_config(f)
            self.config["sprites"][_sprite["name"]] = _sprite

        self.clock_tick_rate = 20
        self.clock = pygame.time.Clock()

        layout = self.config["main"].get("layout", {})
        title = self.config["main"].get("name", "A Yammy game!")
        layout_size = (
            layout.get("width", 640),
            layout.get("height", 480),
        )

        self.screen = pygame.display.set_mode(layout_size)

        # TODO: set a default image
        icon_filename = str(
            get_path("/assets/images") / layout.get("icon")
        )
        icon_image = pygame.image.load(icon_filename)
        pygame.display.set_icon(icon_image)

        # initialize mixer
        pygame.mixer.init()

    def start(self):
        # necessary for using custom fonts
        pygame.init()

        self.next_scene_name = self.config["main"]["initial-scene"]

        self.scenes = Scenes(self)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.scenes.events(event)

            self.scenes.run()