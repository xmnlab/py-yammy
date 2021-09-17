"""Main module template with example functions."""
import os
import sys
from pathlib import Path
from typing import Optional

import pygame
from yammy.scene import ScenesControl
from yammy.settings import get_path
from yammy.utils import read_config


class Yammy:
    config = {}
    scenes_control: Optional[ScenesControl] = None
    # pygame screen
    screen = None
    status: str = "active"

    def __init__(self, project_path: Path):
        os.environ["YAMMY_PROJECT_PATH"] = str(project_path)

        self.config = {}

        self.config = read_config(get_path("/") / "main.yaml")
        self.scenes_control = ScenesControl(self)

        self.clock = pygame.time.Clock()

        layout = self.config.get("layout", {})
        title = self.config.get("title", "A Yammy game!")

        layout_size = (
            layout.get("width", 640),
            layout.get("height", 480),
        )

        self.screen = pygame.display.set_mode(layout_size)

        # TODO: set a default image
        icon_filename = str(get_path("/assets/images") / layout.get("icon"))
        icon_image = pygame.image.load(icon_filename)

        pygame.display.set_icon(icon_image)
        pygame.display.set_caption(title)

        # initialize mixer
        pygame.mixer.init()
        self.status = "active"

    def start(self):
        # necessary for using custom fonts
        pygame.init()

        while self.status == "active":
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                self.scenes_control.events(event)

            self.scenes_control.run()

        pygame.display.quit()
        pygame.quit()
        sys.exit()
