from graphics import TextButton
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

MAIN_MENU_BUTTONS = [
    TextButton(0, 4 * HEADER_FONT_SIZE, "Campaign", 1),
    TextButton(0, 5 * HEADER_FONT_SIZE, "Endless", 1),
    TextButton(0, 6 * HEADER_FONT_SIZE, "Leaderboard", 1),
    TextButton(0, 7 * HEADER_FONT_SIZE, "Achievements", 1),
    TextButton(0, 8 * HEADER_FONT_SIZE, "Settings", 1),
    TextButton(0, 9 * HEADER_FONT_SIZE, "Quit", 1)
]

SCREEN_WIDTH_HALF = SCREEN_WIDTH / 2
for button in MAIN_MENU_BUTTONS:
    _, y = button.current_position
    button.change_position(SCREEN_WIDTH_HALF - (button.width / 2), y)

class MainMenuModel:
    def __init__(self):
        self._screen_change_buttons = MAIN_MENU_BUTTONS
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