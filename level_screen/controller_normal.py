from __future__ import annotations
from .model_normal import GameModel
from .view_normal import GameView
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA
from modes import CampaignModeGameOverCondition, NoEnemiesRoundOverCondition

import pyxel

class GameController:
    def __init__(self, model, view, app):
        self._model = model
        self._view = view
        self._app = app

    def update(self):
        if not self._model.is_current_screen:
            state = self._model.state
            if state in self._app.screens and state != self._model.base_state:
                self.switch_screen(self._model.state)
            else:
                self._model.start_screen()
        else:
            if self._model._game_logic.is_game_over:
                pyxel.quit()

            clicked_btn = self._view.get_clicked_button(self._model.buttons)
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

    def switch_screen(self, state):
        self._app.switch_screen(state)

class GameScreen:
    def __init__(self, app):
        self._model = GameModel(DATA, CampaignModeGameOverCondition(), NoEnemiesRoundOverCondition())
        self._view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._controller = GameController(self._model, self._view, app)

    def start_screen(self):
        self._model.start_screen()

    def update(self):
        self._controller.update()

    def draw(self):
        self._controller.draw()