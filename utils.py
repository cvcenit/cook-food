from enum import StrEnum
import pyxel
import json
from math import pi

with open("settings.json", "r") as f:
    DATA = json.load(f)

FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
HEADER_FONT_SIZE = 64
HEADER_FONT = pyxel.Font("./resources/eater.ttf", font_size=HEADER_FONT_SIZE)

GAMEPLAY_WIDTH = 1000
GAMEPLAY_HEIGHT = 800
GAMEPLAY_X_OFFSET = 280
GAMEPLAY_Y_OFFSET = 0
BULLET_RADIUS = 15

# pixels per second, diagonal length in 5 seconds
BULLET_VELOCITY_MAGNITUDE = ((((GAMEPLAY_WIDTH ** 2) + (GAMEPLAY_HEIGHT ** 2)) ** (1 / 2)) / 5) / FPS

PI = pi

TILE_SIDE_LENGTH = GAMEPLAY_WIDTH / 10 # Pixels, will change

class AppState(StrEnum):
    MAIN_MENU = "main_menu"
    MAIN_SETTINGS = "main_settings"
    MAIN_LEADERBOARDS = "main_leaderboards"
    CAMPAIGN_MENU = "campaign_menu"
    ENDLESS_MENU = "endless_menu"
    GAMEPLAY = "gameplay"
    MAIN_QUIT = "main_quit"