from __future__ import annotations
from .model_achievements import AchievementModel
from .view_achievements import AchievementsView
from .achievements_manager import AchievementManager
from graphics import Screen
from utils import SCREEN_WIDTH, SCREEN_HEIGHT


class AchievementsController:
    def __init__(self, model: AchievementModel, view: AchievementsView, achievement_manager):
        self._model = model
        self._view = view
        self._achievement_manager = achievement_manager

    def get_clicked_screen_change_button(self) -> str | None:
        clicked = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked == 0:
            return "main_menu"
        if clicked == 1:
            self._achievement_manager.reset()
            return None
        
    def update(self):
        clicked_idx = self._view.get_clicked_button(self._model.popup_buttons)
        self._model.update(clicked_idx)
    
    def draw(self):
        self._view.reset_screen()
        self._view.draw_achievements(self._model.achievements)
        self._view.draw_buttons(self._model.screen_change_buttons)

def make_achievements_screen(achievement_manager: AchievementManager) -> Screen:
    model = AchievementModel(achievement_manager)
    view = AchievementsView(SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = AchievementsController(model, view, achievement_manager)
    return Screen(model, view, controller)