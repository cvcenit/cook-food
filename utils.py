from enum import StrEnum
import pyxel
import json
from math import pi

with open("data/settings.json", "r") as f:
    DATA = json.load(f)

with open("data/player_data.json", "r") as f_1:
    PLAYER_DATA = json.load(f_1)

FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
HEADER_FONT_SIZE = 48
CONTENT_FONT_SIZE = 96
HEADER_FONT = pyxel.Font("./resources/Daydream DEMO.otf", font_size=HEADER_FONT_SIZE)
HEADER_FONT_PATH = "./resources/Daydream DEMO.otf"
CONTENT_FONT = pyxel.Font("./resources/Digital808.ttf", font_size=CONTENT_FONT_SIZE)
CONTENT_FONT_PATH = "./resources/Digital808.ttf"

ENEMY_COLORS = [2, 9, 11, 7, 10, 4]

GAMEPLAY_WIDTH = 1000
GAMEPLAY_HEIGHT = 800
GAMEPLAY_X_OFFSET = 280
GAMEPLAY_Y_OFFSET = 0
BULLET_RADIUS = 15

# pixels per second, diagonal length in 5 seconds
BULLET_VELOCITY_MAGNITUDE = ((((GAMEPLAY_WIDTH ** 2) + (GAMEPLAY_HEIGHT ** 2)) ** (1 / 2)) / 5) / FPS

PI = pi

TILE_SIDE_LENGTH = GAMEPLAY_WIDTH / 11 # Pixels, will change

class AppState(StrEnum):
    MAIN_MENU = "main_menu"
    MAIN_SETTINGS = "main_settings"
    MAIN_LEADERBOARDS = "main_leaderboards"
    CAMPAIGN_MENU = "campaign_menu"
    ENDLESS_MENU = "endless_menu"
    ENDLESS_GAMEPLAY = "endless_gameplay"
    ENDLESS_GAMEPLAY_2 = "endless_gameplay_2"
    ENDLESS_GAMEPLAY_3 = "endless_gameplay_3"
    ENDLESS_GAMEPLAY_4 = "endless_gameplay_4"
    ENDLESS_GAMEPLAY_5 = "endless_gameplay_5"
    GAMEPLAY = "gameplay"
    GAMEPLAY_2 = "gameplay_2"
    GAMEPLAY_3 = "gameplay_3"
    GAMEPLAY_4 = "gameplay_4"
    GAMEPLAY_5 = "gameplay_5"
    MAIN_QUIT = "main_quit"
    SETTINGS = "main_settings"
    MAIN_ACHIEVEMENTS = "main_achievements"
    MAIN_SHOP = "main_shop"
    