from __future__ import annotations
from model import GameModel
from view import GameView

import pyxel

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def update(self):
        if self._model._is_game_over:
            pyxel.quit()

        self._model.update()

    def draw(self):
        self._view.reset_screen()
        # disable this kung ayaw m nung gumagalaw
        self._view.draw_enemies(self._model.enemies)

    def run(self):
        pyxel.init(self._view._width, self._view._height)
        pyxel.mouse(visible=True) 
        pyxel.run(self.update, self.draw)
    