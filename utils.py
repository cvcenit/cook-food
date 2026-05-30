from enum import StrEnum
import pyxel
import json
from math import pi # will definetly include more later

with open("settings.json", "r") as f:
    DATA = json.load(f)

FPS = 30
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 800
HEADER_FONT_SIZE = 48
HEADER_FONT = pyxel.Font("./resources/eater.ttf", font_size=HEADER_FONT_SIZE)

# TO ADD: "Gameplay screen dimensions", parang square tas nasa gilid/taas ung buttons and other stuff
GAMEPLAY_WIDTH = 800
GAMEPLAY_HEIGHT = 600
GAMEPLAY_X_OFFSET = 280 + 100
GAMEPLAY_Y_OFFSET = 100
BULLET_RADIUS = 15 # pixels
BULLET_VELOCITY_MAGNITUDE = ((((GAMEPLAY_WIDTH ** 2) + (GAMEPLAY_HEIGHT ** 2)) ** (1 / 2)) / 5) / FPS # pixels per second, diagonal length in 5 seconds
PI = pi

TILE_SIDE_LENGTH = GAMEPLAY_HEIGHT / 10 # Pixels, will change

class AppState(StrEnum):
    MAIN_MENU = "main_menu"
    MAIN_SETTINGS = "main_settings"
    MAIN_LEADERBOARDS = "main_leaderboards"
    CAMPAIGN_MENU = "campaign_menu"
    ENDLESS_MENU = "endless_menu"
    GAMEPLAY = "gameplay"
    MAIN_QUIT = "main_quit"


def rectangles_has_collided(rect_one, rect_two) -> bool:
    x1, y1, w1, h1 = rect_one
    x2, y2, w2, h2 = rect_two
    return True
    # x and y positions are top left corner

def rectangle_and_circle_has_collided(rect, circ) -> bool:
    x_circ, y_circ, r = circ
    x_rect, y_rect, w, h = rect
    return True