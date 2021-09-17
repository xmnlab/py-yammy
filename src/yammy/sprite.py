import glob

from yammy.settings import get_path
from yammy.utils import read_config


class SpritesControl:
    @classmethod
    def get_sprites(cls, something):
        sprites = {}
        for f in glob(str(get_path("/sprites") / "*.spr.yaml")):
            sprite = read_config(f)
            sprites[sprite["name"]] = sprite

        return sprites


class Sprite:

    file_path: str = ""

    def __init__(self, file_path: str):
        self.file_path = file_path
