from __future__ import annotations
from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, HEADER_FONT, CONTENT_FONT, SCREEN_WIDTH
from graphics import TextGraphic
import pyxel

class GameView:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height
        self._bg_color: int = 0
        self._left_margin: float = self._width / 10
        self._top_margin: float = self._height / 4

        self._tower_mode = TextGraphic(25, 150, "", 1, size=24)

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

    def draw_craters(self, craters):
        for x, y in craters:
            pyxel.blt(
            x - 16,
            y - 16,
            2,
            64, 32,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
            )

    # might change this to another popupscreen
    def draw_sidebar(self, buttons, round: int, exp: int, lives: int, placing_tower: bool, not_enough_exp: bool, speed_multiplier: int, purchased_items):
        pyxel.rect(0, 0, 280, 800, 13)
        pyxel.text(30, 200, f"RND: {round}", 1, font=CONTENT_FONT)
        pyxel.text(30, 248, f"EXP: {exp}", 1, font=CONTENT_FONT)
        pyxel.text(30, 296, f"LIVES: {lives}", 1, font=CONTENT_FONT)
        if placing_tower:
            if not_enough_exp:
                y = "LOW EXP!"
            else:
                y = "PLACING..."
            self._tower_mode.change_text(y)
            if not self._tower_mode.is_active:
                self._tower_mode.toggle_active()
            self._tower_mode.draw_text()
        else:
            if self._tower_mode.is_active:
                self._tower_mode.toggle_active()

        if speed_multiplier == 2:
            pyxel.text(500, 700, "2X SPEED", 10, font=HEADER_FONT)

        for i, button in enumerate(buttons):
            if i == 1 and 2 not in purchased_items:
                button.change_color(5)
            elif i == 1:
                button.change_color(10)
            button.draw_button()
    
    def draw_popups(self, popups):
        for popup in popups:
            popup.draw_background()
            popup.draw_popup()

    def draw_achievement_popup(self, achievement):
        if achievement:
            title = "ACHIEVEMENT UNLOCKED!"
            title_x = (SCREEN_WIDTH - HEADER_FONT.text_width(title)) // 2
            pyxel.text(title_x, 20, title, 10, font=HEADER_FONT)
            
            name_x = (SCREEN_WIDTH - HEADER_FONT.text_width(achievement.title)) // 2
            pyxel.text(name_x, 80, achievement.title, 7, font=HEADER_FONT)
    
    def draw_register_message(self, message):
        if message:
            pyxel.text(
                (SCREEN_WIDTH - HEADER_FONT.text_width(message)) // 2,
                600,
                message,
                10,
                font=HEADER_FONT
            )

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
