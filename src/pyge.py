"""Main module template with example functions."""
import io
import base64
from pathlib import Path

import PySimpleGUI as sg
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
    def __init__(self, project_path: Path):
        self.paths["project"] = project_path
        self.paths["assets"] = self.paths["project"] / "assets"

        self.config = {}

        with open(self.paths["project"] / "main.yaml", "r") as f:
            self.config["main"] = yaml.load(f)

        with open(self.paths["project"] / "sprites.yaml", "r") as f:
            self.config["sprites"] = yaml.load(f)

    def start(self):
        layout = self.config["main"].get("layout", {})
        title = self.config["main"].get("name", "A PyGE game!")
        layout_auto_size = layout.get("auto_size", False)

        if not layout_auto_size:
            layout_size = (
                layout.get("width", 640),
                layout.get("height", 480),
            )

        content = []

        if layout.get("background"):
            filename = str(self.paths["assets"] / layout.get("background"))
            content.append([sg.Image(data=convert_to_bytes(filename))])

        params = dict(
            title=title,
            layout=content,
            margins=(0, 0),
            background_color="#000000",
        )

        if not layout_auto_size:
            params["size"] = layout_size


        if layout.get("icon"):
            params["icon"] = str(
                self.paths["assets"] / "media" /
                "images" / layout.get("icon")
            )

        # print(params)

        window = sg.Window(**params)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            print('You entered ', values[0])

        window.close()
