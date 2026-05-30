from .model_main_menu import StartMenuModel
from .view_main_menu import StartMenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import Screen

import pyxel

class StartMenuController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.buttons)
        self._model.update(clicked_idx)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_buttons(self._model.buttons)

model = StartMenuModel()
view = StartMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = StartMenuController(model, view)

MainMenuScreen = Screen(model, view, controller)