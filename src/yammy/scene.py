import pygame

from yammy import layout
from yammy.timer import Timer
from yammy.sound import SoundBoard
from yammy.layout import Layout
from yammy.utils import read_config
from yammy.settings import get_path


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
            filepath = get_path("/scenes") / f"{scene_name}.scn.yaml"
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
