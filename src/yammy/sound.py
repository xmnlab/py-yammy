import pygame

from yammy.settings import get_path


class SoundBoard:
    parent = None
    soundtrack = None
    sound = None

    def __init__(self, parent):
        self.parent = parent
        self.soundtrack = SoundTrack(self.parent)
        self.sound = Sound(self.parent)

    def run(self):
        self.soundtrack.play()


class SoundTrack:
    parent = None
    active = False

    def __init__(self, parent):
        self.parent = parent

    def play(self):
        if self.active:
            return

        self.active = False
        if self.parent.scene.get("soundtrack"):
            soundtrack_filename = str(
                get_path("/assets/audios")
                / self.parent.scene.get("soundtrack")
            )
            pygame.mixer.music.load(soundtrack_filename)
            self.active = True
            pygame.mixer.music.play(-1)

    def stop(self):
        if self.active:
            pygame.mixer.music.stop()
            self.active = False


class Sound:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def play(self):
        ...
