"""Main module template with example functions."""
import io
import base64
import os
from pathlib import Path
import sys
import time

import pygame
import yaml

from pyge.scene import Scenes
from pyge.utils import read_config


class PyGE:
    paths = {}
    config = {}
    clock_tick_rate = 20

    scene = None
    scenes = None
    soundtrack = None
    next_scene_name = None

    screen = None

    def __init__(self, project_path: Path):
        os.environ["PYGE_PROJECT_PATH"] = str(project_path)

        self.paths["project"] = project_path
        self.paths["assets"] = self.paths["project"] / "assets"
        self.paths["scenes"] = self.paths["project"] / "scenes"

        self.config = {}

        self.config["main"] = read_config(self.paths["project"] / "main.yaml")
        self.config["sprites"] = read_config(
            self.paths["project"] / "sprites.yaml"
        )
        self.config["scenes"] = read_config(
            self.paths["project"] / "scenes.yaml"
        )

        self.clock_tick_rate = 20
        self.clock = pygame.time.Clock()

        layout = self.config["main"].get("layout", {})
        title = self.config["main"].get("name", "A PyGE game!")
        layout_size = (
            layout.get("width", 640),
            layout.get("height", 480),
        )

        self.screen = pygame.display.set_mode(layout_size)

        # TODO: set a default image
        icon_filename = str(
            self.paths["assets"] / "images" / layout.get("icon")
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
