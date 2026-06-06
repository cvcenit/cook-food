from .model_main_menu import MainMenuModel
from .view_main_menu import MainMenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import Screen

import pyxel

class MainMenuController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["campaign_mode", "endless_mode", "main_leaderboards", "main_achievements", "main_shop", "main_settings", "main_quit"]
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None:
            return actions[clicked_btn]

    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.popup_buttons)
        self._model.update(clicked_idx)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_buttons(self._model.popup_buttons)

model = MainMenuModel()
view = MainMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = MainMenuController(model, view)

MainMenuScreen = Screen(model, view, controller)