from .model_shop import ShopModel
from .view_shop import ShopView
from achievements import AchievementManager
from graphics import Screen
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class ShopController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["main_menu"]
        clicked = self._view.get_clicked_buttons(self._model.screen_change_buttons)
        if clicked is not None:
            return actions[clicked]
        
    def update(self):
        clicked = self._view.get_clicked_buttons(self._model.item_buttons)
        if clicked is not None:
            self._model.buy(clicked)
        self._model.update(clicked)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_title()
        self._view.draw_points(self._model._achievements.points)
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_items(self._model.item_buttons, self._model.purchased)
        self._view.draw_message(self._model.message)

def make_shop_screen(achievements: AchievementManager):
    model = ShopModel(achievements)
    view = ShopView(SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = ShopController(model, view)
    return Screen(model, view, controller)