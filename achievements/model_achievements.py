from __future__ import annotations
from .achievements_manager import AchievementManager
from graphics import TextButton
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

BACK_BUTTON = TextButton(0, SCREEN_HEIGHT - 100, "Back to menu", 7, size=48)
_, _y = BACK_BUTTON.current_position
BACK_BUTTON.change_position((SCREEN_WIDTH - BACK_BUTTON.width) / 2, _y)

RESET_BUTTON = TextButton(0, SCREEN_HEIGHT - 100, "Reset", 7, size=48)
_, _y = RESET_BUTTON.current_position
RESET_BUTTON.change_position((SCREEN_WIDTH // 2 + 400), _y)


class AchievementModel:
    def __init__(self, achievement_manager: AchievementManager):
        self._achievement_manager = achievement_manager
        self._screen_change_buttons = [BACK_BUTTON, RESET_BUTTON]
        self._popup_buttons = []
        self._current_tick = 1

    @property
    def screen_change_buttons(self):
        return self._screen_change_buttons
    
    @property
    def popup_buttons(self):
        return self._popup_buttons
    
    @property
    def current_tick(self):
        return self._current_tick
    
    @property
    def achievements(self) -> dict:
        return self._achievement_manager.achievements
    
    def update(self, clicked_idx):
        self._current_tick += 1

    def start_screen(self):
        self._current_tick = 1

    def reset(self):
        self.start_screen()