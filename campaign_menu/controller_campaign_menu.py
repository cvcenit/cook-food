from .model_campaign_menu import CampaignMenuModel
from .view_campaign_menu import CampaignMenuView
from utils import SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import Screen

import pyxel

class CampaignMenuController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["main_menu", *[f"level_{i + 1}" for i in range(len(self._model._levels))]]
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None:
            return actions[clicked_btn]

    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.popup_buttons)
        self._model.update(clicked_idx)

    def draw(self):
        self._view.reset_screen()
        pyxel.load("resources/bg.pyxres")
        self._view.draw_background()
        pyxel.load("resources/sprites.pyxres")
        self._view.draw_texts(self._model.texts)
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_buttons(self._model.popup_buttons)
        self._view.draw_characters()

model = CampaignMenuModel([1, 2, 3, 4, 5])
view = CampaignMenuView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = CampaignMenuController(model, view)

CampaignMenuScreen = Screen(model, view, controller)