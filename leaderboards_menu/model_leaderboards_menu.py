from graphics import TextButton, TextGraphic, PopupScreen
from utils import HEADER_FONT_SIZE, PLAYER_DATA, SCREEN_WIDTH
from math import ceil

import pyxel


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

COLUMN_WIDTHS = [50, 400, 150, 150, 150]
X_OFFSETS = [0, 50, 450, 600, 750]
PLAYERS_PER_PAGE = 10
class LeaderboardRow:
    def __init__(self, x, y, column_values, color):
        self._column_widths = COLUMN_WIDTHS
        self._column_values = column_values
        self._x_offsets = X_OFFSETS
        assert len(self._column_values) == len(self._column_widths) == len(self._x_offsets)

        self._x, self._y = x, y
        self._color = color
        self._load_texts()

    @property
    def texts(self):
        return self._texts

    def _load_texts(self):
        self._texts = []
        for i, val in enumerate(self._column_values):
            text = str(val)
            c = TextGraphic(self._x + self._x_offsets[i] + 10, self._y - 5, text, 0, size=24)
            c.toggle_active()
            self._texts += [c]

    def draw_row(self):
        pyxel.rect(self._x, self._y, 900, 40, self._color)

class LeaderboardsMenuModel:
    def __init__(self):
        self._sort_by = "total"
        self._keys = ["name", "campaign_completed_rounds", "endless_highest_rounds", "total"]
        self._screen_change_buttons = SCREEN_CHANGE_BUTTONS
        self._popup_buttons = POPUP_BUTTONS
        self._data = PLAYER_DATA
        self._current_tick = 1
        self._current_page = 1

        self._players = self.players
        self._last_page = ceil(len(self._players) / PLAYERS_PER_PAGE)
        self._row_per_page = {}
        self._header_row = self.leaderboard_headers()
        self._current_rows = self.leaderboard_players()
        self._texts = self.leaderboard_texts


        self._popup_inside = PopupScreen(165, 75, 950, 475, [], self._texts, 12)
        self._popup_inside.toggle_active()
        self._popup_screens = [popup_main, self._popup_inside]

    @property
    def leaderboard_texts(self):
        res = []
        for row in self.leaderboard_rows:
            res += row.texts
        return res

    @property
    def leaderboard_rows(self):
        return [self._header_row] + self._current_rows
    
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
        if self._sort_by == "total":
            return [p[0] for p in sorted(self._data.items(),
                    key=lambda x: x[1]["campaign_completed_rounds"] + x[1]["endless_highest_rounds"], reverse=True)]
        else:
            return [p[0] for p in sorted(self._data.items(), key=lambda x: x[1][self._sort_by], reverse=True)]

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

    def leaderboard_headers(self):
        column_values = ["#", "Player Name", "Campaign", "Endless", "Total"]
        return LeaderboardRow(190, 75, column_values, 12)

    def leaderboard_players(self):
        if self.current_page not in self._row_per_page:
            starting_player = PLAYERS_PER_PAGE * (self.current_page - 1)
            upper_bound = starting_player + PLAYERS_PER_PAGE
            rows = []
            for i, player in enumerate(self.players[starting_player:upper_bound]):
                index = starting_player + i + 1
                player_data = self._data[player]
                campaign_completed_rounds = player_data["campaign_completed_rounds"]
                endless_highest_rounds = player_data["endless_highest_rounds"]
                total = campaign_completed_rounds + endless_highest_rounds
                column_values = [index, player, campaign_completed_rounds, endless_highest_rounds, total]
                row = LeaderboardRow(190, 75 + (40 * (i + 1) + (3 * i)), column_values, i + 1)
                rows += [row]
            self._row_per_page[self.current_page] = rows
        return self._row_per_page[self.current_page]

    def update(self, clicked_idx):
        self._current_tick += 1
        if clicked_idx is not None:
            match clicked_idx:
                case 0:
                    self.previous_page()
                case _:
                    self.next_page()

            self._current_rows = self.leaderboard_players()
            self._texts = self.leaderboard_texts
            self._popup_inside.change_texts(self._texts)

    def start_screen(self):
        self._current_tick = 1
        self._current_page = 1
        self._current_rows = self.leaderboard_players()
        self._texts = self.leaderboard_texts
        self._popup_inside.change_texts(self._texts)

    def reset(self):
        self.start_screen()