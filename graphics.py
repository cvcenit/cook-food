from abc import ABC, abstractmethod
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_FONT_SIZE, HEADER_FONT

import pyxel

class Button(ABC):
    @abstractmethod
    def is_clicked(self) -> bool:
        ...

    @abstractmethod
    def is_hovered(self) -> bool: ...

    @abstractmethod
    def draw_button(self) -> None: ...

class TextButton(Button):
    def __init__(self, x, y, text, color, size=HEADER_FONT_SIZE):
    	#TODO: make it possible to use different fonts/font sizes by D.I.?? ang arte tlg ng term
        self._x, self._y, self._text, self._color = x, y, text, color
        self._size = size
        self._font = pyxel.Font("./resources/eater.ttf", font_size=self._size)
        self._text_width = self._font.text_width(self._text)
        self._is_active = True

    @property
    def text_width(self):
        return self._text_width

    def toggle_active(self):
        self._is_active = not self._is_active

    def is_clicked(self) -> bool:
        if self._is_active:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                if self.is_hovered():
                    return True
            return False

    def is_hovered(self):
        if self._is_active:
            return self._x <= pyxel.mouse_x <= self._x + self._text_width and \
            self._y + 0.5 * self._size <= pyxel.mouse_y <= self._y + 1.4 * self._size

    def draw_button(self):
        if self._is_active:
            pyxel.text(self._x, self._y, self._text, (8 if self.is_hovered() else self._color), font=self._font)

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