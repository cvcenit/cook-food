from abc import ABC, abstractmethod
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_FONT_SIZE, HEADER_FONT

import pyxel

class Button(ABC):
    @abstractmethod
    def is_clicked(self) -> bool:
        ...

    @abstractmethod
    def is_hovered(self) -> bool:
        ...

class TextButton(Button):
    def __init__(self, x, y, text, color):
    	#TODO: make it possible to use different fonts/font sizes by D.I.?? ang arte tlg ng term
        self._x, self._y, self._text, self._color = x, y, text, color
        self._text_width = HEADER_FONT.text_width(self._text)

    @property
    def text_width(self):
        return self._text_width

    def is_clicked(self) -> bool:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.is_hovered():
                return True
        return False

    def is_hovered(self):
        return self._x <= pyxel.mouse_x <= self._x + self._text_width and \
        self._y + 0.5 * HEADER_FONT_SIZE <= pyxel.mouse_y <= self._y + 1.4 * HEADER_FONT_SIZE

    def draw_button(self):
        pyxel.text(self._x, self._y, self._text, (8 if self.is_hovered() else self._color), font=HEADER_FONT)

    @property
    def current_position(self):
        return self._x, self._y

    def change_position(self, x, y):
        self._x = x
        self._y = y

class SpriteButton(Button):
    pass

class Screen:
    def __init__(self, model, view, controller):
        self._model = model
        self._view = view
        self._controller = controller

    def start_screen(self):
        self._model.start_screen()

    def reset(self):
        self._model.reset()
        self.start_screen()

    def get_clicked_button(self):
        return self._controller.get_clicked_screen_change_button()

    def update(self):
        self._controller.update()

    def draw(self):
        self._controller.draw()