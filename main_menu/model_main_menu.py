from graphics import TextButton
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

MAIN_MENU_BUTTONS = [
    TextButton(0, 4 * HEADER_FONT_SIZE, "Campaign", 1),
    TextButton(0, 5 * HEADER_FONT_SIZE + 16, "Endless", 1),
    TextButton(0, 6 * HEADER_FONT_SIZE + 32, "Leaderboard", 1),
    TextButton(0, 7 * HEADER_FONT_SIZE + 48, "Achievements", 1),
    TextButton(0, 8 * HEADER_FONT_SIZE + 64, "Shop", 1),
    TextButton(0, 9 * HEADER_FONT_SIZE + 80, "Settings", 1),
    TextButton(0, 10 * HEADER_FONT_SIZE + 96, "Quit", 1)
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
        self._phase = "title"

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
    def phase(self):
        return self._phase
    
    def advance_to_menu(self):
        self._phase = "menu"

    def update(self, clicked_idx):
        self._current_tick += 1

    def start_screen(self):
        self._current_tick = 1
        self._phase = "title"

    def reset(self):
        self.start_screen()