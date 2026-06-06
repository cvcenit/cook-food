from utils import SCREEN_WIDTH, SCREEN_HEIGHT

import pyxel
from utils import HEADER_FONT, SCREEN_WIDTH, SCREEN_HEIGHT
from graphics import draw_background

class MainMenuView:
    def __init__(self, width, height):
        self._width, self._height = width, height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    def draw_background(self) -> None:
        draw_background()

    def draw_title(self) -> None:
        title = "MERYENDA MAYHEM"
        tw = HEADER_FONT.text_width(title)
        x = (self._width - tw) // 2
        y = self._height // 3
        pyxel.text(x, y, title, 7, font=HEADER_FONT)

        prompt = "click anywhere to start"
        pw = len(prompt) * 4
        pyxel.text((self._width - pw) // 2, y + 90, prompt, 1)

    def draw_buttons(self, buttons) -> None:
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons) -> None | int:
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i
    
    def has_clicked_anywhere(self) -> bool:
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)
        pyxel.blt(
        (SCREEN_WIDTH / 2) - 32, (SCREEN_HEIGHT / 2) - 16,
        0,
        0, 0,
        63, 40,
        0,
        scale=SCREEN_WIDTH/63
        )