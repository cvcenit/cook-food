from __future__ import annotations
from model import GameModel
from view import GameView
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA
from modes import SimpleGameOverCondition, SimpleRoundOverCondition

import pyxel

class GameController:
    def __init__(self, model, view, app):
        self._model = model
        self._view = view
        self._app = app

    def update(self):
        if self._model._is_game_over:
            pyxel.quit()

        self._model.update()

    def draw(self):
        self._view.reset_screen()
        # disable this kung ayaw m nung gumagalaw
        self._view.draw_enemies(self._model.enemies)

    def switch_screen(self, state):
        self._app.switch_screen(state)

    def run(self):
        pyxel.init(self._view._width, self._view._height)
        pyxel.mouse(visible=True) 
        pyxel.run(self.update, self.draw)

class GameScreen:
    def __init__(self, app):
        self._model = GameModel(DATA, SimpleGameOverCondition(), SimpleRoundOverCondition())
        self._view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT)
        self._controller = GameController(self._model, self._view, app)

    def update(self):
        self._controller.update()

    def draw(self):
        self._controller.draw()