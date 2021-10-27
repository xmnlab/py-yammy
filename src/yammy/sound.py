import pygame
from yammy.settings import get_path


class SoundBoard:
    game = None
    soundtrack = None
    sound = None

    def __init__(self, game):
        self.game = game
        self.soundtrack = SoundTrack(self.game)
        self.sound = Sound(self.game)

    def run(self):
        self.soundtrack.play()


class SoundTrack:
    game = None
    active = False

    def __init__(self, game):
        self.game = game

    def play(self):
        if self.active:
            return

        self.active = False

        soundtrack = self.game.scenes_controller.current_scene.config.get(
            "soundtrack"
        )

        if not soundtrack:
            self.stop()
            return

        soundtrack_filename = str(
            get_path("/assets/audios", soundtrack["file"])
        )
        pygame.mixer.music.load(soundtrack_filename)

        self.active = True

        volume = float(soundtrack.get("volume", 50)) / 100.0
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)

    def stop(self):
        if self.active:
            pygame.mixer.music.stop()
            self.active = False


class Sound:
    game = None

    def __init__(self, game):
        self.game = game

    def play(self):
        ...
