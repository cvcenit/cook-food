import pyxel

class CampaignMenuView:
    def __init__(self, width, height):
        self._width, self._height = width, height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    def draw_buttons(self, buttons) -> None:
        for button in buttons:
            button.draw_button()

    def get_clicked_button(self, buttons) -> int:
        for i, button in enumerate(buttons):
            if button.is_clicked():
                return i

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)