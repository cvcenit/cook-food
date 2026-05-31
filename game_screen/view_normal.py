from __future__ import annotations
from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, HEADER_FONT
import pyxel

class GameView:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._bg_color: int = 6
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

    # OUTPUT METHODS
    # CHANGED DRAW ENEMIES FOR SPRITE TESTING
    def draw_enemies(self, enemies) -> None:
        # put the draw in the enemy class
        # for enemy in enemies:
        #     x,y = enemy.position
        #     pyxel.circ(x, y, 25, enemy.sprite)
        for enemy in enemies:
            if enemy.is_alive:
                enemy.draw()

    def draw_towers(self, towers) -> None:
        for tower in towers:
            tower.draw_tower()

    def draw_bullets(self, bullets) -> None:
        for bullet in bullets:
            bullet.draw_bullet()

    def draw_buttons(self, buttons):
        for button in buttons:
            button.draw_button()

    def draw_player(self, player):
        player.draw_tower()

    # CHANGED TO GRID DRAW TO COLOR THE TILES GREEN VALID TILES AND RED INVALID TILES
    def draw_grid(self, grid) -> None:
#        for i in range(1, 8):
#            for j in range(11):
#                pyxel.rectb(GAMEPLAY_X_OFFSET + (j * TILE_SIDE_LENGTH), GAMEPLAY_Y_OFFSET + (i * TILE_SIDE_LENGTH), TILE_SIDE_LENGTH, TILE_SIDE_LENGTH, 1)
        grid.draw()

    def draw_sidebar(self, buttons, exp: int, lives: int, placing_tower: bool, not_enough_exp: bool):
        pyxel.rect(0, 0, 280, 800, 3)
        pyxel.text(10, 500, f"EXP: {exp}", 7, font=HEADER_FONT)
        pyxel.text(10, 580, f"LIVES: {lives}", 7, font=HEADER_FONT)
        if placing_tower:
            if not_enough_exp:
                pyxel.text(10, 700, "NOT ENOUGH EXP!", 7, font=HEADER_FONT)
            else:
                pyxel.text(10, 700, "PLACING TOWER...", 7, font=HEADER_FONT)
        for button in buttons:
            button.draw_button()

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)

    # ---------------------------------------
    # "INPUT" METHODS
    def get_clicked_button(self, buttons) -> None | int:
        for i, button in enumerate(buttons):
            if button.is_clicked():
                return i

    def get_mouse_position(self) -> tuple[float, float]:
        return pyxel.mouse_x, pyxel.mouse_y

    def has_left_clicked(self) -> bool:
        return pyxel.btnp((pyxel.MOUSE_BUTTON_LEFT))