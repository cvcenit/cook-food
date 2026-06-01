from graphics import TextButton, TextGraphic, PopupScreen
from utils import HEADER_FONT_SIZE, PLAYER_DATA, SCREEN_WIDTH

buttons = []
texts = []
popup = PopupScreen(140, 50, 1000, 600, buttons, texts, 2)
popup.toggle_active()

SCREEN_CHANGE_BUTTONS = [TextButton(0, 678, "Back", 1, size=48)]
for button in SCREEN_CHANGE_BUTTONS:
    x, y = button.current_position
    x = (SCREEN_WIDTH / 2) - (button.text_width / 2)
    button.change_position(x, y)


class LeaderboardsMenuModel:
    def __init__(self):
        self._screen_change_buttons = SCREEN_CHANGE_BUTTONS
        self._popup_buttons = []
        self._data = PLAYER_DATA
        self._popup_screens = [popup]

        self._current_tick = 1
        self._is_current_screen = True

    @property
    def screen_change_buttons(self):
        return self._screen_change_buttons

    @property
    def popup_buttons(self):
        return self._popup_buttons

    @property
    def popup_screens(self):
        return self._popup_screens
    
    @property
    def current_tick(self):
        return self._current_tick

    def leaderboard_column_headers(self):
        ...

    def leaderboard_players(self):
        ...

    def update(self, clicked_idx):
        self._current_tick += 1

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1

    def reset(self):
        self.start_screen()