from __future__ import annotations

import glob
import os
from typing import Optional

import pygame
from yammy.layout import Layout
from yammy.settings import get_path
from yammy.sound import SoundBoard
from yammy.sprite import SpritesController
from yammy.timer import Timer
from yammy.utils import read_config


class ScenesController:
    config: dict = {}
    scenes: list[Scene] = []
    current_scene: Optional[Scene] = None
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
        self.new(scene_name)

    def play(self):
        if self.current_scene.status == "finished":
            next_scene_name = self.current_scene.config.get("next-scene")
            if not next_scene_name:
                self.game.status = "finished"
                return

            self.goto(next_scene_name)

        self.current_scene.play()

        pygame.display.update()

        self.game.clock.tick(self.game.config.get("clock-tick-rate"))

    def events(self, event):
        for ev in self.current_scene.events_trigger:
            try:
                ev(event, self.game)
            except Exception as e:
                import pdb

                pdb.set_trace()
                print(e)


class Scene:

    config: dict = {}
    status = "active"  # options: active, finished

    def __init__(self, game, name):
        self.game = game
        self.timer = Timer(self)
        self.soundboard = SoundBoard(self.game)
        self.layout = Layout(self.game)
        self.events_trigger = []

        self.current_name = name

        filepath = get_path("/scenes") / f"{name}.scn.yaml"
        self.config = read_config(filepath)
        self.sprites = SpritesController(self.config.get("sprites"))

        self.events_trigger.extend(self.sprites.get_events())

    def play(self):
        self.timer.check_ending()

        # soundtrack
        self.soundboard.run()

        # background
        # TODO: Show just when the background need to be updated
        self.layout.background.show()
        self.layout.update()
        self.sprites.render(self.game.screen)

        self.timer.check_begining()
        self.timer.update_counter()
