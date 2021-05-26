"""Main module template with example functions."""
from pathlib import Path
import PySimpleGUI as sg
import yaml


class PyGE:
    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.config = {}

        with open(project_path / "main.yaml", "r") as f:
            self.config["main"] = yaml.load(f)

        with open(project_path / "sprites.yaml", "r") as f:
            self.config["main"] = yaml.load(f)

    def start(self):
        layout = self.config["main"].get("layout", {})
        title = self.config["main"].get("name", "A PyGE game!")
        layout_auto_size = layout.get("auto_size", False)

        if not layout_auto_size:
            layout_size = (
                layout.get("width", 640),
                layout.get("height", 480),
            )

        params = dict(
            title=title,
            layout=[[]],
            margins=(100, 50),
        )

        if not layout_auto_size:
            params["size"] = layout_size

        window = sg.Window(**params)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == 'Cancel': # if user closes window or clicks cancel
                break
            print('You entered ', values[0])

        window.close()
