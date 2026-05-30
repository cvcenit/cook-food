from __future__ import annotations

from campaign_menu.controller_campaign_menu import CampaignMenuScreen
from game_screen.controller_normal import LevelMenuScreen
from main_menu.controller_main_menu import MainMenuScreen
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA, AppState

import pyxel

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
        pyxel.run(self.update, self.draw)

SCREENS = {
    AppState.MAIN_MENU: MainMenuScreen,
    AppState.CAMPAIGN_MENU: CampaignMenuScreen,
    AppState.GAMEPLAY: LevelMenuScreen
    }

ROUTES = {
    AppState.MAIN_MENU: {
    "campaign_mode": AppState.CAMPAIGN_MENU,
    "endless_mode": AppState.ENDLESS_MENU,
    "main_settings": AppState.MAIN_SETTINGS,
    "main_leaderboards": AppState.MAIN_LEADERBOARDS,
    "main_quit": AppState.MAIN_QUIT
    },

    AppState.CAMPAIGN_MENU: {
    "main_menu": AppState.MAIN_MENU,
    "level_1": AppState.GAMEPLAY
    },
    
    AppState.GAMEPLAY: {
    "campaign_mode": AppState.CAMPAIGN_MENU
    }
}

g = Game(SCREENS, ROUTES)
if __name__ == "__main__":
    g.run()