from .start_model import StartMenuModel
from .start_view import StartMenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import Screen

import pyxel


class StartMenuController:
    def __init__(self, model, view, app):
        self._model = model
        self._view = view
        self._app = app

    def update(self):
        if not self._model.is_current_screen:
            state = self._model.state
            if state in self._app.screens and state != self._model.base_state:
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

class StartMenuScreen(Screen):
    def __init__(self, app):
        self._app = app
        self._model = StartMenuModel()
        self._view = StartMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._controller = StartMenuController(self._model, self._view, self._app)

    def start_screen(self):
        self._model.start_screen()

    def update(self):
        self._controller.update()

    def draw(self):
        self._controller.draw()