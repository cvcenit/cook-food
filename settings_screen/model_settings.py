from graphics import TextButton
from utils import HEADER_FONT_SIZE, SCREEN_WIDTH, HEADER_FONT, DATA
import json

SETTINGS_BUTTONS = [
    TextButton(0, 1 * HEADER_FONT_SIZE, "Back", 1),
    TextButton(0, 9 * HEADER_FONT_SIZE, "Save", 1),
]


# TOO MUCH CODE REPETITION GOING ON HERE SRY WILL FIX TOMO TOLOG N Q -janella
LIVES_DECREASE_BUTTON = TextButton(0, 4 * HEADER_FONT_SIZE, "<", 1)
LIVES_INCREASE_BUTTON = TextButton(0, 4 * HEADER_FONT_SIZE, ">", 1)
ENEMIES_DECREASE_BUTTON = TextButton(0, 6 * HEADER_FONT_SIZE, "<", 1)
ENEMIES_INCREASE_BUTTON = TextButton(0, 6 * HEADER_FONT_SIZE, ">", 1)
REGENERATOR_DECREASE_BUTTON = TextButton(0, 8 * HEADER_FONT_SIZE, "<", 1)
REGENERATOR_INCREASE_BUTTON = TextButton(0, 8 * HEADER_FONT_SIZE, ">", 1)

ARROW_BUTTONS = [
    LIVES_DECREASE_BUTTON, 
    LIVES_INCREASE_BUTTON,
    ENEMIES_DECREASE_BUTTON,
    ENEMIES_INCREASE_BUTTON,
    REGENERATOR_DECREASE_BUTTON,
    REGENERATOR_INCREASE_BUTTON
]

SCREEN_WIDTH_HALF = SCREEN_WIDTH / 2
for button in SETTINGS_BUTTONS + ARROW_BUTTONS:
    _, y = button.current_position
    button.change_position(SCREEN_WIDTH_HALF - (button.text_width / 2), y)


lives_width = HEADER_FONT.text_width("Lives:  _")
enemies_width = HEADER_FONT.text_width("Enemies:  _")
regenerator_width = HEADER_FONT.text_width("Regenerator Interval:  _")
arrow_width = HEADER_FONT.text_width("<")
gap = 8


LIVES_DECREASE_BUTTON.change_position(SCREEN_WIDTH_HALF - lives_width // 2 - gap - arrow_width, 3 * HEADER_FONT_SIZE)
LIVES_INCREASE_BUTTON.change_position(SCREEN_WIDTH_HALF + lives_width // 2 + gap, 3 * HEADER_FONT_SIZE)
ENEMIES_DECREASE_BUTTON.change_position(SCREEN_WIDTH_HALF - enemies_width // 2 - gap - arrow_width, 5 * HEADER_FONT_SIZE)
ENEMIES_INCREASE_BUTTON.change_position(SCREEN_WIDTH_HALF + enemies_width // 2 + gap, 5 * HEADER_FONT_SIZE)
REGENERATOR_DECREASE_BUTTON.change_position(SCREEN_WIDTH_HALF - regenerator_width // 2 - gap - arrow_width, 7 * HEADER_FONT_SIZE)
REGENERATOR_INCREASE_BUTTON.change_position(SCREEN_WIDTH_HALF + regenerator_width // 2 + gap, 7 * HEADER_FONT_SIZE)


class SettingsModel:
    def __init__(self):
        self._screen_change_buttons = SETTINGS_BUTTONS
        self._current_tick = 1
        self._lives = 2
        self._enemies = 5
        self._regenerator_interval = 3
        self._lives_decrease_button = LIVES_DECREASE_BUTTON
        self._lives_increase_button = LIVES_INCREASE_BUTTON
        self._enemies_decrease_button = ENEMIES_DECREASE_BUTTON
        self._enemies_increase_button = ENEMIES_INCREASE_BUTTON
        self._regenerator_decrease_button = REGENERATOR_DECREASE_BUTTON
        self._regenerator_increase_button = REGENERATOR_INCREASE_BUTTON

    @property
    def screen_change_buttons(self):
        return self._screen_change_buttons
    
    @property
    def lives(self):
        return self._lives

    @property
    def lives_decrease_button(self):
        return self._lives_decrease_button

    @property
    def lives_increase_button(self):
        return self._lives_increase_button

    def increase_lives(self):
        if self._lives < 5:
            self._lives += 1

    def decrease_lives(self):
        if self._lives > 1:
            self._lives -= 1

    @property
    def enemies(self):
        return self._enemies

    @property
    def enemies_decrease_button(self):
        return self._enemies_decrease_button

    @property
    def enemies_increase_button(self):
        return self._enemies_increase_button

    def increase_enemies(self):
        self._enemies += 1

    def decrease_enemies(self):
        if self._enemies > 1:
            self._enemies -= 1
    
    @property
    def regenerator_interval(self):
        return self._regenerator_interval

    @property
    def regenerator_decrease_button(self):
        return self._regenerator_decrease_button

    @property
    def regenerator_increase_button(self):
        return self._regenerator_increase_button

    def increase_regenerator(self):
        self._regenerator_interval += 1

    def decrease_regenerator(self):
        if self._regenerator_interval > 1:
            self._regenerator_interval -= 1

    def save(self):
        DATA["remaining_lives"] = self._lives
        DATA["remaining_enemies"] = self._enemies
        DATA["regenerator_interval"] = self._regenerator_interval
        with open("settings.json", "w") as f:
            json.dump(DATA, f) # or not ? dapat ba isave sa settings o hnd
    
    def reset(self):
        self._current_tick = 1
    
    def start_screen(self):
        self._current_tick = 1
    
    def update(self, clicked_idx):
        self._current_tick = 1
    