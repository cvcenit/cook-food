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
        
        self.check_all_enemies_gone()
        self.check_game_over()
        self._model.update()
    
    def check_all_enemies_gone(self):
        if self._model.number_of_enemies <= 0:
            self._model._is_game_over = True

    def check_game_over(self):
        if self._model.lives <= 0:
            self._model._is_game_over = True

    def start_game(self):
        self._view.start_game(self, self)

    def draw(self):
        self._view.reset_screen()
        # disable this kung ayaw m nung gumagalaw
        self._view.draw_enemies(self._model.enemies)