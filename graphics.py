from abc import ABC, abstractmethod
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_FONT_SIZE, HEADER_FONT

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
        self._x, self._y, self._text, self._color = x, y, text, color
        self._text_width = HEADER_FONT.text_width(self._text)

    def is_clicked(self) -> bool:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.is_hovered():
            	return True
        return False

    def is_hovered(self):
        return self._x <= pyxel.mouse_x <= self._x + self._text_width and \
        1.25 * self._y <= pyxel.mouse_y <= self._y + 1.5 * HEADER_FONT_SIZE

    def draw_button(self):
        pyxel.text(self._x, self._y, self._text, (8 if self.is_hovered() else self._color), font=HEADER_FONT)

class SpriteButton(Button):
    pass

class Screen(ABC):
    @abstractmethod
    def update(self):
        ...    

    @abstractmethod
    def draw(self):
        ...

class MainMenuModel:
    def __init__(self):
        self._buttons = [
        TextButton(48, 48, "Play", 1),
        TextButton(48, 96, "Settings", 1)
        ]
        self._states = ["play", "settings"]
        self._current_tick = 1
        self._is_current_screen = True
        self._state = "main"

    @property
    def is_current_screen(self):
        return self._is_current_screen

    @property
    def buttons(self):
        return self._buttons
    
    @property
    def state(self):
        return self._state

    @property
    def current_tick(self):
        return self._current_tick

    def update(self, clicked_idx):
        if self._is_current_screen:
            self._current_tick += 1
            if clicked_idx is not None:
                self.change_screen(self._states[clicked_idx])

    def change_screen(self, state):
        self._is_current_screen = False
        self._current_tick = 1
        self._state = state

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1
        self._state = "main"

class MainMenuView:
    def __init__(self, width, height):
        self._width, self._height = width, height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    def draw_buttons(self, buttons) -> None:
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons) -> int:
    	for i, button in enumerate(buttons):
    		if button.is_clicked():
    			return i

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)

class MainMenuController:
    def __init__(self, model, view, app):
        self._model = model
        self._view = view
        self._app = app

    def update(self):
        if self._model.state == "main":
            self._model.start_screen()

        if not self._model.is_current_screen:
        	state = self._model.state
        	if state in self._app.screens:
	            self.switch_screen(self._model.state)
	        else:
	        	self._model.start_screen()

        clicked_idx = self._view.get_clicked_button(self._model.buttons)
        self._model.update(clicked_idx)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_buttons(self._model.buttons)

    def switch_screen(self, state):
        self._app.switch_screen(state)

class MainMenuScreen(Screen):
    def __init__(self, app):
        self._app = app
        self._model = MainMenuModel()
        self._view = MainMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._controller = MainMenuController(self._model, self._view, self._app)

    def update(self):
        self._controller.update()

    def draw(self):
        self._controller.draw()


class GridLayout:
    # ang demanding
    pass