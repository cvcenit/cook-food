from .model_leaderboards_menu import LeaderboardsMenuModel
from .view_leaderboards_menu import LeaderboardsMenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import Screen

import pyxel

class LeaderboardsMenuController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["main_menu",]
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None:
            return actions[clicked_btn]

    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.popup_buttons)
        self._model.update(clicked_idx)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_popup_screens(self._model.popup_screens, self._model.leaderboard_rows)
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_buttons(self._model.popup_buttons)

LeaderboardsMenuModelInstance = LeaderboardsMenuModel()
view = LeaderboardsMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = LeaderboardsMenuController(LeaderboardsMenuModelInstance, view)

LeaderboardsMenuScreen = Screen(LeaderboardsMenuModelInstance, view, controller)