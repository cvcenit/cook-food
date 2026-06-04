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
    def draw_enemies(self, enemies, tunnels: set) -> None:
        for enemy in enemies:
            if enemy.is_alive:
                enemy_tile = enemy._path[enemy._path_index]
                in_tunnel = enemy_tile in tunnels
                enemy.draw(in_tunnel)

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
        grid.draw()

    # might change this to another popupscreen
    def draw_sidebar(self, buttons, round: int, exp: int, lives: int, placing_tower: bool, not_enough_exp: bool):
        pyxel.rect(0, 0, 280, 800, 13)
        pyxel.text(10, 136, f"RND: {round}", 7, font=HEADER_FONT)
        pyxel.text(10, 200, f"EXP: {exp}", 7, font=HEADER_FONT)
        pyxel.text(10, 264, f"LIVES: {lives}", 7, font=HEADER_FONT)
        if placing_tower:
            if not_enough_exp:
                pyxel.text(10, 400, "NOT ENOUGH EXP!", 7, font=HEADER_FONT)
            else:
                pyxel.text(10, 400, "PLACING TOWER...", 7, font=HEADER_FONT)
        for button in buttons:
            button.draw_button()
    
    def draw_popups(self, popups):
        for popup in popups:
            popup.draw_background()
            popup.draw_popup()

    def reset_screen(self) -> None:
        pyxel.cls(self._bg_color)

    # ---------------------------------------
    # "INPUT" METHODS
    def get_clicked_button(self, buttons) -> None | int:
        for i, button in enumerate(buttons):
            if button.is_left_clicked():
                return i

    def get_clicked_tower(self, towers) -> None | int:
        for i, tower in enumerate(towers):
            if tower.is_right_clicked():
                return i

    def get_mouse_position(self) -> tuple[float, float]:
        return pyxel.mouse_x, pyxel.mouse_y

    def get_tower_direction(self):
        if pyxel.btnp(pyxel.KEY_W):
            return "w"
        elif pyxel.btnp(pyxel.KEY_S):
            return "s"
        elif pyxel.btnp(pyxel.KEY_D):
            return "d"
        elif pyxel.btnp(pyxel.KEY_A):
            return "a"
        else:
            return None
    
    def has_left_clicked(self) -> bool:
        return pyxel.btnp((pyxel.MOUSE_BUTTON_LEFT))

    def has_right_clicked(self) -> bool:
        return pyxel.btnp((pyxel.MOUSE_BUTTON_RIGHT))
