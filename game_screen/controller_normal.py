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

    def get_clicked_screen_change_button(self):
        actions = ["campaign_mode"]
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None:
            return actions[clicked_btn]

    def update(self):
        if self._model._game_logic.is_game_over:
            pyxel.quit()

        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        clicked = self._view.has_left_clicked()

        # just gets current direction
        mouse_x, mouse_y = self._view.get_mouse_position()
        player_x, player_y = self._model._game_logic.player.screen_position()
        cardinal_x, cardinal_y = (mouse_x - player_x), -(mouse_y - player_y)
        direction = atan2(cardinal_y, cardinal_x)

        self._model._game_logic.player_change_direction(direction)
        self._model._game_logic.player.load_next_bullet(direction)
        if clicked:
            self._model._game_logic.player_shoot()

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            self._model._game_logic.try_place_tower(mouse_x, mouse_y)
        
        self._model.update(clicked_btn)

    def draw(self):
        self._view.reset_screen()
        # JOWEE BASAHIN E2
        # palitan ang laman ng draw_grid, ipass ang level as argument or kahit fields ng level
        # mag aadd ka rin ng valid tiles at invalid tiles at player tile sa level data 
        # imatch ung color ng in/valid tower tiles, path tile, player tile
        self._view.draw_grid(self._model._game_logic.grid)

        # draw entities
        self._view.draw_towers(self._model._game_logic.towers)
        self._view.draw_player(self._model._game_logic.player)
        self._view.draw_enemies(self._model._game_logic.enemies)
        self._view.draw_bullets(self._model._game_logic.bullets)

        # draw ui + buttons
        self._view.draw_sidebar(self._model.sidebar_buttons)
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_buttons(self._model.popup_buttons)

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