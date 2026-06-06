import pyxel
from utils import HEADER_FONT, HEADER_FONT_SIZE, CONTENT_FONT, CONTENT_FONT_SIZE
from graphics import draw_background

class SettingsView:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._bg_color = 6
        self._smooth_movement_x = 0
    
    def draw_background(self) -> None:
        draw_background()

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons):
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i

    def draw_lives_label(self, lives):
        label_x = self._width // 2 - CONTENT_FONT.text_width("Lives:  _") // 2
        pyxel.text(label_x, 3 * (CONTENT_FONT_SIZE - 30), f"Lives: {lives}", 1, font=CONTENT_FONT)
    
    def draw_enemies_label(self, enemies):
        label_x = self._width // 2 - CONTENT_FONT.text_width("Enemies:  _") // 2
        pyxel.text(label_x, 4 * (CONTENT_FONT_SIZE - 30), f"Enemies: {enemies}", 1, font=CONTENT_FONT)

    def draw_regenerator_label(self, regenerator_interval):
        label_x = self._width // 2 - CONTENT_FONT.text_width("Regenerator Interval:   _") // 2
        pyxel.text(label_x, 5 * (CONTENT_FONT_SIZE - 30), f"Regenerator Interval: {regenerator_interval}", 1, font=CONTENT_FONT)

    def draw_chameleon_label(self, chameleon_interval):
        label_x = self._width // 2 - CONTENT_FONT.text_width("Chameleon Interval:  _") // 2
        pyxel.text(label_x, 6 * (CONTENT_FONT_SIZE - 30), f"Chameleon Interval: {chameleon_interval}", 1, font=CONTENT_FONT)

    def draw_smooth_movement(self, smooth_movement):
        box_size = CONTENT_FONT_SIZE - 42
        gap = 1
        total_width = box_size + gap + CONTENT_FONT.text_width("Smooth Movement")
        
        self._smooth_movement_x = self._width // 2 - total_width // 2

        pyxel.rectb(self._smooth_movement_x - 10, 7 * (CONTENT_FONT_SIZE - 30) + 15, box_size, box_size, 1)
        pyxel.rectb(self._smooth_movement_x - 9, 7 * (CONTENT_FONT_SIZE - 30) + 16, box_size - 2, box_size - 2, 1)
        if smooth_movement:
            pyxel.text(self._smooth_movement_x  + 1, 7 * (CONTENT_FONT_SIZE - 30) + 1, "x", 1, font=CONTENT_FONT)
        pyxel.text(self._smooth_movement_x  + box_size + gap, 7 * (CONTENT_FONT_SIZE - 30), "Smooth Movement", 1, font=CONTENT_FONT)

    def draw_guide_popup(self, popup):
        popup.draw_background()
        popup.draw_popup()

    def is_decrease_clicked(self):
        label_x = self._width // 2 - 30
        label_y = self._height // 2
        x, y = label_x - 16, label_y
        return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 
                x <= pyxel.mouse_x <= x + 8 and y <= pyxel.mouse_y <= y + 8)

    def is_increase_clicked(self):
        label_x = self._width // 2 - 30
        label_y = self._height // 2
        x, y = label_x + 40, label_y
        return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 
                x <= pyxel.mouse_x <= x + 8 and y <= pyxel.mouse_y <= y + 8)

    def is_smooth_movement_clicked(self):
        box_size = CONTENT_FONT_SIZE
        x = self._smooth_movement_x - 8
        y = 7 * (CONTENT_FONT_SIZE - 30) + 3
        return (pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and 
                x <= pyxel.mouse_x <= x + box_size and
                y <= pyxel.mouse_y <= y + box_size)

    def reset_screen(self):
        pyxel.cls(self._bg_color)
