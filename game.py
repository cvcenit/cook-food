from __future__ import annotations

from achievements import AchievementManager
from achievements_menu.controller_achievements import make_achievements_screen
from campaign_menu.controller_campaign_menu import CampaignMenuScreen
from game_screen.controller_normal import make_level_screen
from leaderboards_menu.controller_leaderboards_menu import LeaderboardsMenuScreen
from main_menu.controller_main_menu import MainMenuScreen
from settings_screen.controller_settings import SettingsScreen
from shop.controller_shop import make_shop_screen

from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA, AppState

import pyxel

shared_achievements = AchievementManager()

class Game:
    def __init__(self, screens: dict[AppState, Screen], routes: dict[AppState, dict[str, AppState]]):
        self._screens = screens
        self._routes = routes

        self._current_state = AppState.MAIN_MENU
        self._current_screen = self._screens[self._current_state]

    def _switch_screen(self, state: AppState):
        if state == AppState.MAIN_QUIT:
            pyxel.quit()

        self._current_state = state
        self._current_screen = self._screens[state]
        self._current_screen.reset()

    def update(self):
        self._current_screen.update()
        clicked_button = self._current_screen.get_clicked_button()

        if clicked_button is not None:
            possible_next_state = self._routes.get(self._current_state, {})
            if clicked_button in possible_next_state:
                self._switch_screen(possible_next_state[clicked_button])

    def draw(self):
        self._current_screen.draw()

    def run(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, fps=FPS)
        pyxel.mouse(visible=True)
        pyxel.load("my_resource.pyxres")
        pyxel.load("bg.pyxres")
        pyxel.run(self.update, self.draw)

SCREENS = {
    AppState.MAIN_MENU: MainMenuScreen,
    AppState.CAMPAIGN_MENU: CampaignMenuScreen,
    AppState.GAMEPLAY: make_level_screen(shared_achievements, "level1"),
    AppState.GAMEPLAY_2: make_level_screen(shared_achievements, "level2"),
    AppState.GAMEPLAY_3: make_level_screen(shared_achievements, "level3"),
    AppState.GAMEPLAY_4: make_level_screen(shared_achievements, "level4"),
    AppState.GAMEPLAY_5: make_level_screen(shared_achievements, "level5"),
    AppState.MAIN_LEADERBOARDS: LeaderboardsMenuScreen,
    AppState.MAIN_SETTINGS: SettingsScreen,
    AppState.MAIN_ACHIEVEMENTS: make_achievements_screen(shared_achievements),
    AppState.MAIN_SHOP: make_shop_screen(shared_achievements),
    AppState.ENDLESS_GAMEPLAY: make_level_screen(shared_achievements, "endless"),
    }

ROUTES = {
    AppState.MAIN_MENU: {
        "campaign_mode": AppState.CAMPAIGN_MENU,
        "endless_mode": AppState.ENDLESS_GAMEPLAY,
        "main_settings": AppState.MAIN_SETTINGS,
        "main_achievements": AppState.MAIN_ACHIEVEMENTS,
        "main_shop": AppState.MAIN_SHOP,
        "main_leaderboards": AppState.MAIN_LEADERBOARDS,
        "main_quit": AppState.MAIN_QUIT
    },

    AppState.CAMPAIGN_MENU: {
        "main_menu": AppState.MAIN_MENU,
        "level_1": AppState.GAMEPLAY,
        "level_2": AppState.GAMEPLAY_2,
        "level_3": AppState.GAMEPLAY_3,
        "level_4": AppState.GAMEPLAY_4,
        "level_5": AppState.GAMEPLAY_5,
    },

    AppState.ENDLESS_GAMEPLAY: {
    "endless_mode": AppState.MAIN_MENU,
    "main_menu": AppState.MAIN_MENU,
    },
    
    AppState.GAMEPLAY: {
        "main_menu": AppState.MAIN_MENU, 
        "campaign_mode": AppState.CAMPAIGN_MENU,
        "endless_mode": AppState.MAIN_MENU, 
    },

    AppState.GAMEPLAY_2: {"main_menu": AppState.MAIN_MENU, "campaign_mode": AppState.CAMPAIGN_MENU},
    AppState.GAMEPLAY_3: {"main_menu": AppState.MAIN_MENU, "campaign_mode": AppState.CAMPAIGN_MENU},
    AppState.GAMEPLAY_4: {"main_menu": AppState.MAIN_MENU, "campaign_mode": AppState.CAMPAIGN_MENU},
    AppState.GAMEPLAY_5: {"main_menu": AppState.MAIN_MENU, "campaign_mode": AppState.CAMPAIGN_MENU},

    AppState.MAIN_LEADERBOARDS: {
        "main_menu": AppState.MAIN_MENU,
    },

    AppState.MAIN_SETTINGS: {
        "main_menu": AppState.MAIN_MENU,
        "save": AppState.MAIN_MENU
    },

    AppState.MAIN_ACHIEVEMENTS: {
        "main_menu": AppState.MAIN_MENU,
    },

    AppState.MAIN_SHOP: {
        "main_menu": AppState.MAIN_MENU,
    },
    
}

g = Game(SCREENS, ROUTES)
if __name__ == "__main__":
    g.run()