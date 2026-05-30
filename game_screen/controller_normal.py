from __future__ import annotations
from .model_normal import GameModel
from .view_normal import GameView
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA, PI
from modes import CampaignMode, EndlessMode, CampaignModeGameOverCondition, EndlessModeGameOverCondition, NoEnemiesRoundOverCondition
from math import atan2
from graphics import Screen

import pyxel

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def update(self):
        if self._model._game_logic.is_game_over:
            pyxel.quit()

        clicked_btn = self._view.get_clicked_button(self._model.buttons)
        clicked = self._view.get_clicked()
        mouse_x, mouse_y = self._view.get_mouse_position()
        cardinal_x, cardinal_y = (mouse_x - (SCREEN_WIDTH / 2)), -(mouse_y - (SCREEN_HEIGHT / 2))
        direction = atan2(cardinal_y, cardinal_x)

        self._model._game_logic.player_change_direction(direction)
        if clicked:
            self._model._game_logic.player_shoot(direction)

        # enemy_hit = self._view.get_hitted_enemy(self._model.enemies, self._model.active_bullets)
        self._model.update(clicked_btn)

    def draw(self):
        self._view.reset_screen()
        self._view.draw_grid()
        self._view.draw_towers(self._model._game_logic.towers)
        self._view.draw_player(self._model._game_logic.player)
        self._view.draw_enemies(self._model._game_logic.enemies)
        self._view.draw_buttons(self._model.buttons)
        self._view.draw_bullets(self._model._game_logic.bullets)

mode = "campaign"

if mode == "campaign":
    level = CampaignMode(DATA)
    game_over = CampaignModeGameOverCondition()
else:
    level = EndlessMode(DATA)
    game_over = EndlessModeGameOverCondition()

model = GameModel(level, game_over, NoEnemiesRoundOverCondition())
view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT)
controller = GameController(model, view)

LevelMenuScreen = Screen(model, view, controller)