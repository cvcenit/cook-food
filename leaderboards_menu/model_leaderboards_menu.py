from graphics import TextButton, TextGraphic, PopupScreen
from utils import HEADER_FONT_SIZE, PLAYER_DATA, SCREEN_WIDTH
from math import ceil


next_button = TextButton(0, 550, "Next", 6, size=48)
n_x, n_y = next_button.current_position
n_x += 1115 - next_button.text_width
next_button.change_position(n_x, n_y)

POPUP_BUTTONS = [
    TextButton(175, 550, "Previous", 6, size=48),
    next_button
]

popup_main = PopupScreen(140, 50, 1000, 600, POPUP_BUTTONS, [], 1)
popup_main.toggle_active()

SCREEN_CHANGE_BUTTONS = [TextButton(0, 678, "Back", 1, size=48)]
for button in SCREEN_CHANGE_BUTTONS:
    x, y = button.current_position
    x = (SCREEN_WIDTH / 2) - (button.text_width / 2)
    button.change_position(x, y)


# column widths are fixed to:
# ill add later

COLUMN_WIDTHS = []
PLAYERS_PER_PAGE = 10
class LeaderboardRow:
    def __init__(self, x, y, column_values, color):
        self._column_widths = COLUMN_WIDTHS
        self._column_values = column_values
        assert len(self._column_values) == len(self._column_widths)

        self._x, self._y = x, y
        self._color = color
        self._load_texts()

    @property
    def texts(self):
        return self._texts

    def _load_texts(self):
        self._texts = []

    def draw_row(self):
        ...

class LeaderboardsMenuModel:
    def __init__(self):
        self._screen_change_buttons = SCREEN_CHANGE_BUTTONS
        self._popup_buttons = POPUP_BUTTONS
        self._data = PLAYER_DATA

        self._players = [p for p in self._data]

        self._texts = []

        self._popup_inside = PopupScreen(165, 75, 950, 475, [], self._texts, 6)
        self._popup_inside.toggle_active()
        self._popup_screens = [popup_main, self._popup_inside]
        
        self._current_tick = 1
        self._current_page = 1
        self._last_page = ceil(len(self._players) / PLAYERS_PER_PAGE)

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

    @property
    def players(self):
        return self._players

    @property
    def current_page(self):
        return self._current_page

    @property
    def current_texts(self):
        return self._current_texts

    def next_page(self):
        self._current_page = min(self._last_page, self._current_page + 1)

    def previous_page(self):
        self._current_page = max(1, self._current_page - 1)

    def leaderboard_column_headers(self):
        ...

    def leaderboard_players(self):
        ...

    def update(self, clicked_idx):
        print(self.current_page)
        self._current_tick += 1
        if clicked_idx is not None:
            if clicked_idx == 0:
                self.previous_page()
            else:
                self.next_page()

    def start_screen(self):
        self._current_tick = 1

    def reset(self):
        self.start_screen()