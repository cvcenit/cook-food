from __future__ import annotations

from level_screen.level_controller import GameScreen
from start_menu.start_screen import StartMenuScreen
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA

import pyxel

class Game:
    def __init__(self):
        self._screens = {
        "main": StartMenuScreen(self),
        "play": GameScreen(self),
        }
        self._state = "main"

    @property
    def screens(self):
        return self._screens

    @property
    def state(self):
        return self._state

    def switch_screen(self, state):
        if state in self._screens:
            self._state = state
            self._screens[self._state].start_screen()

    def update(self):
        self._screens[self._state].update()

    def draw(self):
        self._screens[self._state].draw()

    def run(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        pyxel.mouse(visible=True) 
        pyxel.run(self.update, self.draw)

g = Game()
if __name__ == "__main__":
    g.run()