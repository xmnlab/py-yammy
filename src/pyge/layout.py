from pathlib import Path

import pygame

from pyge import settings


class Layout:
    parent = None

    def __init__(self, parent):
        self.parent = parent
        self.background = Background(self.parent)
        self.elements = {}

    def new(self):
        self.elements = {}

    def update(self):
        expansion = self.parent.scene.get("expansion")

        if not expansion:
            return

        for item in expansion.get("layout", {}).get("elements", {}):
            name = item["name"]
            if name in self.elements:
                ...

            if item["type"] == "button":
                # it should use the font from font/source or font/family

                self.elements[name] = Button(
                    item["text"],
                    (item["x"], item["y"]),
                    style=item.get("style"),
                )
                self.elements[name].show(self.parent.screen)
                self.parent.scenes.events_trigger.append(
                    self.elements[name].click
                )


class Background:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def show(self):
        if self.parent.scene.get("background"):
            background_filename = str(
                self.parent.paths["assets"]
                / self.parent.scene.get("background")
            )
            background_image = pygame.image.load(background_filename).convert()
            self.parent.screen.blit(background_image, [0, 0])


class Font:
    @classmethod
    def get(cls, style):
        # default
        font_size = 30
        font_class = pygame.font.SysFont
        font_source = "Arial"

        if not style:
            return font_class(font_source, font_size)

        if style.get("font-source"):
            font_class = pygame.font.Font
            font_source = str(settings.get_path("fonts") / style["font-source"])
        elif style.get("font-family"):
            font_class = pygame.font.SysFont
            font_source = style["font-family"]

        if style.get("font-size"):
            font_size = int(style["font-size"])

        return font_class(font_source, font_size)

class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, text, pos, feedback="", style={}):
        self.x, self.y = pos

        # font
        self.font = Font.get(style)

        if feedback == "":
            self.feedback = "text"
        else:
            self.feedback = feedback
        self.change_text(text, "black")

    def change_text(self, text, bg="black"):
        """Change the text whe you click"""
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        self.surface = pygame.Surface(self.size)
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def show(self, screen):
        screen.blit(self.surface, (self.x, self.y))

    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    self.change_text(str(self.feedback), bg="red")
                print("button clicked")
