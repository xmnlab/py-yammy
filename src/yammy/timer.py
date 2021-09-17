class Timer:
    def __init__(self, parent):
        self.parent = parent
        self.counter = None

    def check_ending(self):
        if self.counter is not None and self.counter <= 0:
            self.parent.next_scene_name = self.parent.scene.get("next-scene")
            self.parent.scene = None
            self.counter = None

    def check_begining(self):
        # timer
        if self.counter is None and not self.parent.scene.get("loop", False):
            # if "loop" is false or not define, "time" should be given
            self.counter = self.parent.scene.get("time")

    def update_counter(self):
        if self.counter is not None:
            self.counter -= self.parent.clock_tick_rate / 200
