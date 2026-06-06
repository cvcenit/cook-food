from graphics import TextButton, TextGraphic
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

LEVEL_BUTTONS = [
    TextButton(48, HEADER_FONT_SIZE, "Back", 3, size=38),
    TextButton(280, 5 * (HEADER_FONT_SIZE + 16), "Level 1", 3),
    TextButton(280, 10 * (HEADER_FONT_SIZE + 16), "Level 2", 3),
    TextButton(1000, 5 * (HEADER_FONT_SIZE + 16), "Level 3", 3),
    TextButton(1000, 10 * (HEADER_FONT_SIZE + 16), "Level 4", 3),
    TextButton(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) + HEADER_FONT_SIZE + 16, "Level 5", 3)
]

SHADOW_TEXT = [
    TextGraphic(53, HEADER_FONT_SIZE + 5, "Back", 1, size=38),
    TextGraphic(285, 5 * (HEADER_FONT_SIZE + 16) + 5, "Level 1", 1, size=HEADER_FONT_SIZE),
    TextGraphic(285, 10 * (HEADER_FONT_SIZE + 16) + 5, "Level 2", 1, size=HEADER_FONT_SIZE),
    TextGraphic(1005, 5 * (HEADER_FONT_SIZE + 16) + 5, "Level 3", 1, size=HEADER_FONT_SIZE),
    TextGraphic(1005, 10 * (HEADER_FONT_SIZE + 16) + 5, "Level 4", 1, size=HEADER_FONT_SIZE),
    TextGraphic(5 + (SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2) + HEADER_FONT_SIZE + 21, "Level 5", 1, size=HEADER_FONT_SIZE)
]

for btn in LEVEL_BUTTONS[1:]:
    x, y = btn.current_position
    btn.change_position(x - (btn.width / 2), y)

for txt in SHADOW_TEXT[1:]:
    x, y = txt.current_position
    txt.change_position(x - (txt.width / 2), y)

class CampaignMenuModel:
    def __init__(self, levels):
        self._levels = levels
        self._screen_change_buttons = LEVEL_BUTTONS
        self._popup_buttons = []
        self._texts = SHADOW_TEXT

        self._current_tick = 1
        self._is_current_screen = True

    @property
    def texts(self):
        return self._texts
    

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