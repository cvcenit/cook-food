import pyxel
from utils import HEADER_FONT, HEADER_FONT_SIZE

class SettingsView:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._bg_color = 6

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons):
        for i, button in enumerate(buttons):
            if button.is_clicked():
                return i

    def draw_lives_label(self, lives):
        label_x = self._width // 2 - HEADER_FONT.text_width("Lives:  _") // 2
        pyxel.text(label_x, 3 * HEADER_FONT_SIZE, f"Lives: {lives}", 1, font=HEADER_FONT)
    
    def draw_enemies_label(self, enemies):
        label_x = self._width // 2 - HEADER_FONT.text_width("Enemies:  _") // 2
        pyxel.text(label_x, 5 * HEADER_FONT_SIZE, f"Enemies: {enemies}", 1, font=HEADER_FONT)

    def draw_regenerator_label(self, regenerator_interval):
        label_x = self._width // 2 - HEADER_FONT.text_width("Regenerator Interval:  _") // 2
        pyxel.text(label_x, 7 * HEADER_FONT_SIZE, f"Regenerator Interval: {regenerator_interval}", 1, font=HEADER_FONT)

    def is_decrease_clicked(self):
        label_x = self._width // 2 - 30
        label_y = self._height // 2
        x, y = label_x - 16, label_y
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and x <= pyxel.mouse_x <= x + 8 and y <= pyxel.mouse_y <= y + 8

    def is_increase_clicked(self):
        label_x = self._width // 2 - 30
        label_y = self._height // 2
        x, y = label_x + 40, label_y
        return pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and x <= pyxel.mouse_x <= x + 8 and y <= pyxel.mouse_y <= y + 8

    def reset_screen(self):
        pyxel.cls(self._bg_color)
