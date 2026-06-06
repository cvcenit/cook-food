from utils import HEADER_FONT, SCREEN_WIDTH, CONTENT_FONT, CONTENT_FONT_PATH
from graphics import draw_background
import pyxel

class ShopView:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._bg_color = 6
    
    def draw_background(self) -> None:
        draw_background()
    
    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw_button()

    def draw_items(self, item_buttons, purchased: set):
        for i, button in enumerate(item_buttons):
            if i in purchased:
                button.change_color(3)
            else:
                button.change_color(1)
            button.draw_button()

    def draw_message(self, message):
        if message:
            x = (SCREEN_WIDTH - CONTENT_FONT.text_width(message)) // 2
            pyxel.text(x, 700, message, 8, font=CONTENT_FONT)

    def draw_title(self):
        title = "SHOP"
        x = (SCREEN_WIDTH - CONTENT_FONT.text_width(title)) // 2
        pyxel.text(x, 200, title, 1, font=HEADER_FONT)

    def draw_points(self, points):
        text = f"Points: {points}"
        x = (SCREEN_WIDTH - CONTENT_FONT.text_width(text)) // 2
        pyxel.text(x, 275, text, 1, font=pyxel.Font(CONTENT_FONT_PATH, font_size=84))

    def get_clicked_buttons(self, buttons):
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i
            
    def reset_screen(self):
        pyxel.cls(self._bg_color)
