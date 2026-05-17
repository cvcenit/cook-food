from __future__ import annotations

import pyxel

class GameView:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    def draw_enemies(self, enemies) -> None:
        for enemy in enemies:
            x,y = enemy.position
            pyxel.circ(x, y, 25, enemy.sprite)

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)