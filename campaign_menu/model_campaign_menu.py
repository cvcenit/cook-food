from graphics import TextButton
from utils import HEADER_FONT_SIZE

# problem in mind: popup buttons and buttons that will change screen has some conflict
# solution: create two different methods for popup buttons and change screen buttons

# TODO: lagay endless mode at campaign mode sa main menu

class CampaignMenuModel:
    def __init__(self, levels):
        self._levels = levels
        self._screen_change_buttons = []
        self._screen_change_buttons += [TextButton(48, HEADER_FONT_SIZE, "Back", 1)]
        for i, level in enumerate(self._levels):
            self._screen_change_buttons.append(TextButton(48, (i + 2) * HEADER_FONT_SIZE, f"Level {i + 1}", 1))

        self._popup_buttons = []

        self._current_tick = 1
        self._is_current_screen = True

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
        ...