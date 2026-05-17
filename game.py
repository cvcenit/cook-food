from __future__ import annotations
from entities import Chef
from model import GameModel
from view import GameView
from controller import GameController

import pyxel
import json

with open("settings.json", "r") as f:
    DATA = json.load(f)

FPS = 30
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720

game = GameController(GameModel(DATA), GameView(SCREEN_WIDTH, SCREEN_HEIGHT))
game.start_game()