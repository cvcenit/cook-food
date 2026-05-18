from __future__ import annotations
from entities import Chef
from model import GameModel
from view import GameView
from controller import GameScreen
from modes import SimpleGameOverCondition, SimpleRoundOverCondition
from graphics import MainMenuScreen
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA

import pyxel

#game.run()

class Game:
    def __init__(self):
        self._screens = {
        "main": MainMenuScreen(self),
        "play": GameScreen(self),
        }
        self._state = "main"

    @property
    def screens(self):
        return self._screens

    def switch_screen(self, state):
        if state in self._screens:
            self._state = state

    def update(self):
        self._screens[self._state].update()

    def draw(self):
        self._screens[self._state].draw()

    def run(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT)
        pyxel.mouse(visible=True) 
        pyxel.run(self.update, self.draw)

g = Game()
g.run()