from __future__ import annotations

import glob
import os
from typing import Optional

import pygame
from yammy.layout import Layout
from yammy.settings import get_path
from yammy.sound import SoundBoard
from yammy.sprite import SpritesControl
from yammy.timer import Timer
from yammy.utils import read_config


class ScenesControl:
    config: dict = {}
    scenes: list = []
    current_scene: Optional[Scene] = None
    next_scene: Optional[Scene] = None
    timer: Optional[Timer] = None

    def __init__(self, game):
        self.game = game
        self.new(self.game.config["initial-scene"])

        for filepath in glob.glob(str(get_path("/scenes") / "*.scn.yaml")):
            name = filepath.split(os.sep)[-1].replace(".scn.yaml", "")
            self.config[name] = read_config(filepath)

    def new(self, scene_name):
        self.current_scene = Scene(self.game, scene_name)

    def goto(self, scene_name):
        self.new(self.game, scene_name)

    def run(self):
        if self.current_scene.status == "finished":
            self.goto(self.game.next_scene_name)

        self.current_scene.timer.check_ending()

        # soundtrack
        self.current_scene.soundboard.run()

        # background
        # TODO: Show just when the background need to be updated
        self.current_scene.layout.background.show()
        self.current_scene.layout.update()

        self.current_scene.timer.check_begining()

        pygame.display.update()

        self.game.clock.tick(self.game.config.get("clock-tick-rate"))
        self.current_scene.timer.update_counter()

    def events(self, event):
        for e in self.current_scene.events_trigger:
            e(event, self.game)


class Scene:

    config: dict = {}
    status = "active"  # options: active, finished

    def __init__(self, game, name):
        self.game = game
        self.timer = Timer(self)
        self.soundboard = SoundBoard(self.game)
        self.layout = Layout(self.game)
        self.events_trigger = []
        self.sprites = SpritesControl.get_sprites(self.game)

        self.current_name = name

        filepath = get_path("/scenes") / f"{name}.scn.yaml"
        self.config = read_config(filepath)
