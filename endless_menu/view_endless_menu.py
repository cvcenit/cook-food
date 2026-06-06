import pyxel
from graphics import draw_background
from utils import TILE_SIDE_LENGTH, HEADER_FONT_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class EndlessMenuView:
    def __init__(self, width, height):
        self._width, self._height = width, height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    def draw_background(self):
        draw_background()

    def draw_texts(self, texts):
        for text in texts:
            text.draw_text()

    def draw_characters(self):
        # taho
        pyxel.blt(
            264,
            3 * (HEADER_FONT_SIZE + 16) + 32,
            1,
            96, 64,
            32, 32,
            3,
            scale=TILE_SIDE_LENGTH/16
        )
        # ihaw
        pyxel.blt(
            264,
            8 * (HEADER_FONT_SIZE + 16) + 32,
            1,
            96, 96,
            32, 32,
            3,
            scale=TILE_SIDE_LENGTH/16
        )
        # sorbetes
        pyxel.blt(
            984,
            3 * (HEADER_FONT_SIZE + 16) + 32,
            1,
            96, 32,
            32, 32,
            3,
            scale=TILE_SIDE_LENGTH/16
        )
        # Pandesal
        pyxel.blt(
            984,
            8 * (HEADER_FONT_SIZE + 16) + 32,
            1,
            96, 128,
            32, 32,
            3,
            scale=TILE_SIDE_LENGTH/16
        )
        # chef
        pyxel.blt(
            SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 32,
            1,
            96, 0,
            32, 32,
            10,
            scale=TILE_SIDE_LENGTH/16
        )

    def draw_buttons(self, buttons) -> None:
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons) -> int:
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)