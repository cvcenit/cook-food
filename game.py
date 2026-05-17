from __future__ import annotations

import pyxel
import json

with open("settings.json", "r") as f:
    DATA = json.load(f)

FPS = 30
SCREEN_WIDTH = 100
SCREEN_HEIGHT = 100


class GameModel:
    def __init__(self):
        self.lives = DATA["remaining_lives"]
        self.enemies = DATA["remaining_enemies"]


class GameView:
    ...


class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view
        self._is_game_over = False

    def update(self):
        if self._is_game_over:
            pyxel.quit()
        
        self.check_all_enemies_gone()
        self.check_game_over()
    
    def check_all_enemies_gone(self):
        if self._model.enemies <= 0:
            self._is_game_over = True

    def check_game_over(self):
        if self._model.lives <= 0:
            self._is_game_over = True

    def draw(self):
        ...

    def run(self):
        pyxel.run(self.update, self.draw)
             