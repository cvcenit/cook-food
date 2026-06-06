from graphics import TextButton
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

LEVEL_BUTTONS = [
    TextButton(280, 5 * (HEADER_FONT_SIZE + 16), "Level 1", 2),
    TextButton(280, 10 * (HEADER_FONT_SIZE + 16), "Level 2", 2),
    TextButton(1000, 5 * (HEADER_FONT_SIZE + 16), "Level 3", 2),
    TextButton(1000, 10 * (HEADER_FONT_SIZE + 16), "Level 4", 2),
    TextButton(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + HEADER_FONT_SIZE + 16, "Level 5", 2)
]

for i, btn in enumerate(LEVEL_BUTTONS):
    x, y = btn.current_position
    btn.change_position(x - (btn.width / 2), y)


class CampaignMenuModel:
    def __init__(self, levels):
        self._levels = levels
        self._screen_change_buttons = []
        self._screen_change_buttons += [TextButton(48, HEADER_FONT_SIZE, "Back", 2, size=38)]
        self._screen_change_buttons += LEVEL_BUTTONS
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