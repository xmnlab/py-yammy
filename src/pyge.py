"""Main module template with example functions."""
import io
import base64
from pathlib import Path
import sys
import time

import pygame
import yaml
import PIL.Image


def convert_to_bytes(file_or_bytes, resize=None):
    '''
    Will convert into bytes and optionally resize an image that is a file or a base64 bytes object.
    Turns into  PNG format in the process so that can be displayed by tkinter
    :param file_or_bytes: either a string filename or a bytes base64 image object
    :type file_or_bytes:  (Union[str, bytes])
    :param resize:  optional new size
    :type resize: (Tuple[int, int] or None)
    :return: (bytes) a byte-string object
    :rtype: (bytes)
    '''
    if isinstance(file_or_bytes, str):
        img = PIL.Image.open(file_or_bytes)
    else:
        try:
            img = PIL.Image.open(io.BytesIO(base64.b64decode(file_or_bytes)))
        except Exception as e:
            dataBytesIO = io.BytesIO(file_or_bytes)
            img = PIL.Image.open(dataBytesIO)

    cur_width, cur_height = img.size
    if resize:
        new_width, new_height = resize
        scale = min(new_height/cur_height, new_width/cur_width)
        img = img.resize((int(cur_width*scale), int(cur_height*scale)), PIL.Image.ANTIALIAS)
    bio = io.BytesIO()
    img.save(bio, format="PNG")
    del img
    return bio.getvalue()


class PyGE:
    paths = {}
    config = {}
    clock_tick_rate = 20

    def __init__(self, project_path: Path):
        self.paths["project"] = project_path
        self.paths["assets"] = self.paths["project"] / "assets"

        self.config = {}

        with open(self.paths["project"] / "main.yaml", "r") as f:
            self.config["main"] = yaml.load(f)

        with open(self.paths["project"] / "sprites.yaml", "r") as f:
            self.config["sprites"] = yaml.load(f)

        with open(self.paths["project"] / "scenes.yaml", "r") as f:
            self.config["scenes"] = yaml.load(f)

        self.clock_tick_rate = 20
        self.clock = pygame.time.Clock()

        layout = self.config["main"].get("layout", {})
        title = self.config["main"].get("name", "A PyGE game!")
        layout_size = (
            layout.get("width", 640),
            layout.get("height", 480),
        )

        self.screen = pygame.display.set_mode(layout_size)

        # TODO: set a default image
        icon_filename =  str(
            self.paths["assets"] / "images" / layout.get("icon")
        )
        icon_image = pygame.image.load(icon_filename)
        pygame.display.set_icon(icon_image)


    def start(self):
        next_scene_name = self.config["main"]["initial-scene"]
        scene = None
        timer = None

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            if timer is not None and timer <= 0:
                next_scene_name = scene["next-scene"]
                scene = None

            if scene is None:
                scene = self.config["scenes"][next_scene_name]
                timer = None

                if not scene.get("loop", False):
                    # if "loop" is false or not define, "time" should be given
                    timer = scene.get("time")


            if scene.get("background"):
                background_filename = str(self.paths["assets"] / scene.get("background"))
                background_image = pygame.image.load(background_filename).convert()
                self.screen.blit(background_image, [0, 0])

            pygame.display.flip()
            self.clock.tick(self.clock_tick_rate)

            if timer is not None:
                timer -= self.clock_tick_rate/200
