import pygame

from pyge import layout
from pyge.timer import Timer
from pyge.sound import SoundBoard
from pyge.layout import Layout
from pyge.utils import read_config


class Scenes:
    def __init__(self, parent):
        self.parent = parent
        self.config = parent.config["scenes"]
        self.timer = Timer(self.parent)
        self.soundboard = SoundBoard(self.parent)
        self.layout = Layout(self.parent)
        self.events_trigger = []
        self.current_scene_name = ""

    def new(self):
        self.layout.new()
        self.events_trigger = []

    def goto(self, scene_name):
        self.new()
        self.current_scene_name = scene_name
        self.parent.scene = self.config[scene_name]

        if self.parent.scene.get("expand", False):
            filepath = self.parent.paths["scenes"] / f"{scene_name}.scn.yaml"
            self.parent.scene["expansion"] = read_config(filepath)

    def run(self):
        self.timer.check_ending()

        if self.parent.scene is None:
            self.goto(self.parent.next_scene_name)

        # soundtrack
        self.soundboard.run()

        # background
        # TODO: Show just when the background need to be updated
        self.layout.background.show()
        self.layout.update()

        self.timer.check_begining()

        pygame.display.update()

        self.parent.clock.tick(self.parent.clock_tick_rate)
        self.timer.update_counter()

    def events(self, event):
        for e in self.events_trigger:
            e(event, self.parent)
