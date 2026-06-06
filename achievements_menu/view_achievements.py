from __future__ import annotations
import pyxel
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, HEADER_FONT


class AchievementsView:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._bg_color = 6
        self._scroll_y = 0
        self._row_height = 160
        self._list_top = 160
        self._list_bottom = SCREEN_HEIGHT - 120
    
    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)

    def draw_buttons(self, buttons) -> None:
        for button in buttons:
            button.draw_button()

    def handle_scroll(self, total_items: int) -> None:
        total_height = total_items * self._row_height
        visible_height = self._list_bottom - self._list_top
        max_scroll = max(0, total_height - visible_height)

        if pyxel.btn(pyxel.KEY_DOWN) or pyxel.mouse_wheel < 0:
            self._scroll_y = min(self._scroll_y + 20, max_scroll)
        if pyxel.btn(pyxel.KEY_UP) or pyxel.mouse_wheel > 0:
            self._scroll_y = max(self._scroll_y - 20, 0)

        # draw scrollbar
        if max_scroll > 0:
            scrollbar_x = SCREEN_WIDTH - 60
            scrollbar_h = self._list_bottom - self._list_top
            thumb_h = max(30, int(scrollbar_h * visible_height / total_height))
            thumb_y = self._list_top + int((scrollbar_h - thumb_h) * self._scroll_y / max_scroll)
            pyxel.rect(scrollbar_x, self._list_top, 8, scrollbar_h, 5)   # track
            pyxel.rect(scrollbar_x, thumb_y, 8, thumb_h, 7)              # thumb

    def draw_achievements(self, achievements: dict) -> None:
        title = "ACHIEVEMENTS"
        pyxel.text((SCREEN_WIDTH - HEADER_FONT.text_width(title)) // 2, 20, title, 7, font=HEADER_FONT)

        self.handle_scroll(len(achievements))

        small_font = pyxel.Font("./resources/Daydream DEMO.otf", font_size=32)

        y_start = self._list_top - self._scroll_y
        for achievement in achievements.values():
            y = y_start
            y_start += self._row_height

            if y < self._list_top or y + self._row_height - 8 > self._list_bottom:
                continue

            pyxel.rectb(80, y, SCREEN_WIDTH - 200, self._row_height - 8, 7)
            if achievement.unlocked:
                pyxel.text(100, y + 15, achievement.title, 10, font=small_font)
                pyxel.text(100, y + 60, achievement.description, 7, font=small_font)
            else:
                pyxel.text(100, y + 15, "???", 5, font=small_font)
    
    def get_clicked_button(self, buttons) -> None | int:
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i