from graphics import TextButton
from utils import HEADER_FONT_SIZE

class MainMenuModel:
    def __init__(self):
        self._screen_change_buttons = [
        TextButton(48, HEADER_FONT_SIZE, "Campaign", 1),
        TextButton(48, 2 * HEADER_FONT_SIZE, "Endless", 1),
        TextButton(48, 3 * HEADER_FONT_SIZE, "Leaderboard", 1),
        TextButton(48, 4 * HEADER_FONT_SIZE, "Settings", 1),
        TextButton(48, 5 * HEADER_FONT_SIZE, "Quit", 1)
        ]
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

    def update(self, clicked_idx):
        self._current_tick += 1

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1

    def reset(self):
        self.start_screen()