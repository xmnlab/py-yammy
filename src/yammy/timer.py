from typing import Optional

from yammy.settings import get_path
from yammy.utils import read_config


class Timer:
    counter: Optional[int] = None

    def __init__(self, scene):
        self.scene = scene
        self.clock_tick_rate = read_config(get_path("/") / "main.yaml")[
            "clock-tick-rate"
        ]
        self.counter = None

    def check_ending(self):
        if self.counter is not None and self.counter <= 0:
            self.scene.status = "finished"
            self.counter = None

    def check_begining(self):
        # timer
        if self.counter is None and not self.scene.config.get("loop", False):
            # if "loop" is false or not define, "time" should be given
            self.counter = self.scene.config.get("time")

    def update_counter(self):
        if self.counter is not None:
            self.counter -= self.clock_tick_rate / 200
