from enum import StrEnum
import pyxel
import json

with open("settings.json", "r") as f:
    DATA = json.load(f)

FPS = 30
SCREEN_WIDTH = 720
SCREEN_HEIGHT = 720
HEADER_FONT_SIZE = 48
HEADER_FONT = pyxel.Font("./eater.ttf", font_size=HEADER_FONT_SIZE)

class MenuState(StrEnum):
    MAIN_MENU = "main"
    MAIN_SETTINGS = "main_settings"
    PLAY_MENU = "play"