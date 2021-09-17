from pathlib import Path

import pygame

from yammy import settings
from yammy.settings import get_path


class Layout:
    parent = None

    def __init__(self, parent):
        self.parent = parent
        self.background = Background(self.parent)
        self.elements = {}
        self.element_type = {"button": Button, "text": Text}

    def new(self):
        self.elements = {}

    def update(self):
        expansion = self.parent.scene.get("expansion")

        if not expansion:
            return

        for item in expansion.get("layout", {}).get("elements", {}):
            name = item["name"]
            class_element = self.element_type.get(item.get("type"))

            if not class_element:
                continue

            self.elements[name] = class_element(item)
            self.elements[name].show(self.parent.screen)

            for k, v in item.get("events", {}).items():
                self.parent.scenes.events_trigger.append(
                    getattr(self.elements[name], k)
                )


class Background:
    parent = None

    def __init__(self, parent):
        self.parent = parent

    def show(self):
        if self.parent.scene.get("background"):
            background_filename = str(
                get_path("/assets")
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
            font_source = str(
                settings.get_path("/assets/fonts") / style["font-source"]
            )
        elif style.get("font-family"):
            font_class = pygame.font.SysFont
            font_source = style["font-family"]

        if style.get("font-size"):
            font_size = int(style["font-size"])

        return font_class(font_source, font_size)


class Button:
    """Create a button, then blit the surface in the while loop"""

    def __init__(self, config):
        self.x = config.get("x", 0)
        self.y = config.get("y", 0)

        self.events = config.get("events", {})

        # font
        self.font = Font.get(config.get("style", {}))

        self.feedback = config.get("feedback", "text")
        self.change_text(config.get("text", "Button"), "black")

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

    def click(self, event, parent):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    eval(f'parent.{self.events["click"]}')


class Text:
    """Create a text, then blit the surface in the while loop"""

    def __init__(self, config):
        self.x = config.get("x", 0)
        self.y = config.get("y", 0)

        self.events = config.get("events", {})

        # font
        self.font = Font.get(config.get("style", {}))

        self.feedback = config.get("feedback", "text")
        self.change_text(config.get("text", "Button"), "black")

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

    def click(self, event, parent):
        if "click" not in self.events:
            return

        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if self.rect.collidepoint(x, y):
                    eval(f'parent.{self.events["click"]}')
