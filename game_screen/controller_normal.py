from __future__ import annotations
from .model_normal import GameModel
from .view_normal import GameView
from entities.towers import Chef, Taho, Pandesal, Sorbetes, Ihaw
from achievements import AchievementManager
from utils import FPS, SCREEN_WIDTH, SCREEN_HEIGHT, DATA, PI, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET
from modes import CampaignMode, EndlessMode, CampaignModeGameOverCondition, EndlessModeGameOverCondition, NoEnemiesRoundOverCondition, Level1, Level2, Level3, Level4, Level5
from math import atan2
from graphics import Screen

import pyxel

class GameController:
    def __init__(self, model, view):
        self._model = model
        self._view = view

    def get_clicked_screen_change_button(self):
        actions = ["campaign_mode",]
        clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
        if clicked_btn is not None: 
            return actions[clicked_btn]
        
        if self._model.game_logic.is_game_over:
            if self._model.game_logic.is_game_won:
                clicked = self._view.get_clicked_button(self._model.popup_screens[4].buttons)
                if clicked == 0:
                    return "main_menu"
            else:
                clicked = self._view.get_clicked_button(self._model.popup_screens[3].buttons)
                if clicked == 0:
                    return "main_menu"

    def get_player_direction(self, pos):
        mouse_x, mouse_y = pos
        player_x, player_y = self._model.game_logic.player.screen_position()
        cardinal_x, cardinal_y = (mouse_x - player_x), -(mouse_y - player_y)
        return atan2(cardinal_y, cardinal_x)

    def update(self):
        if not self._model.game_logic.is_game_over:
            clicked_btn = self._view.get_clicked_button(self._model.screen_change_buttons)
            pause_menu_clicked = self._view.get_clicked_button(self._model.popup_screens[0].buttons)

            self._model.update_from_pause_menu(pause_menu_clicked)
                
            if self._model.is_paused:
                self._model.update(clicked_btn)
                return

            left_clicked = self._view.has_left_clicked()
            right_clicked = self._view.has_right_clicked()
            
            mouse_x, mouse_y = self._view.get_mouse_position()

            direction = self.get_player_direction((mouse_x, mouse_y))

            self._model.game_logic.player_change_direction(direction)
            for i in range(self._model.game_logic.player.tower_level):
                self._model.game_logic.player.load_next_bullet(i)
                
            sidebar_clicked = self._view.get_clicked_button(self._model.sidebar_buttons)
            self._model.update_from_sidebar(sidebar_clicked)

            tower_menu_clicked = self._view.get_clicked_button(self._model.popup_screens[1].buttons)
            self._model.update_from_tower_menu(tower_menu_clicked)

            tower_direction = self._view.get_tower_direction()
            self._model.update_from_direction_menu(tower_direction)
            
            if right_clicked:
                clicked_tower = self._view.get_clicked_tower(self._model.game_logic.towers)
                self._model.update_towers(clicked_tower)

            if left_clicked:
                if (0 <= mouse_x <= GAMEPLAY_X_OFFSET) or (0 <= mouse_y <= GAMEPLAY_Y_OFFSET):
                    ...
                elif self._model.game_logic.placing_tower:
                    self._model.game_logic.place_tower(mouse_x, mouse_y)
                else:
                    self._model.game_logic.player_shoot()
                    
            self._model.update(clicked_btn)
        else:
            self._model.update_game_over()

            if self._model.game_logic.is_game_won:
                win_clicked = self._view.get_clicked_button(self._model.popup_screens[4].buttons)
                if win_clicked == 1:
                    self._model.reset()
                elif win_clicked == 2:
                    self._model.handle_register(4, "campaign")
            else:
                game_over_clicked = self._view.get_clicked_button(self._model.popup_screens[3].buttons)
                if game_over_clicked == 1:
                    self._model.reset()
                elif game_over_clicked == 2:
                    self._model.handle_register(3, "endless")

    def draw(self):
        self._view.reset_screen()
        self._view.draw_grid(self._model.game_logic.grid)

        # draw entities
        self._view.draw_towers(self._model.game_logic.towers)
        self._view.draw_player(self._model.game_logic.player)
        self._view.draw_enemies(self._model.game_logic.enemies, self._model.game_logic.tunnels)
        self._view.draw_bullets(self._model.game_logic.bullets)

        # draw ui + buttons
        self._view.draw_sidebar(self._model.sidebar_buttons, self._model.game_logic.round_index, self._model.game_logic.exp, self._model.game_logic.lives, self._model.game_logic.placing_tower, self._model.game_logic.not_enough_exp)
        self._view.draw_buttons(self._model.screen_change_buttons)
        self._view.draw_popups(self._model.popup_screens)

        self._view.draw_achievement_popup(self._model.game_logic.current_achievement_display)
        self._view.draw_register_message(self._model.register_message)

LEVEL_ONE_AVAILABLE_TOWERS = [Taho,]
LEVEL_TWO_AVAILABLE_TOWERS = LEVEL_ONE_AVAILABLE_TOWERS + [Ihaw]
LEVEL_THREE_AVAILABLE_TOWERS = LEVEL_TWO_AVAILABLE_TOWERS + [Sorbetes]
LEVEL_FOUR_AVAILABLE_TOWERS = LEVEL_THREE_AVAILABLE_TOWERS + [Pandesal]


# todo: make five different levels
def make_level_screen(shared_achievements: AchievementManager, mode):
    if mode == "endless":
        level = EndlessMode(DATA, LEVEL_FOUR_AVAILABLE_TOWERS)
        game_over = EndlessModeGameOverCondition()
    elif mode == "level1":
        level = Level1(DATA, LEVEL_ONE_AVAILABLE_TOWERS)
        game_over = CampaignModeGameOverCondition()
    elif mode == "level2":
        level = Level2(DATA, LEVEL_TWO_AVAILABLE_TOWERS)
        game_over = CampaignModeGameOverCondition()
    elif mode == "level3":
        level = Level3(DATA, LEVEL_THREE_AVAILABLE_TOWERS)
        game_over = CampaignModeGameOverCondition()
    elif mode == "level4":
        level = Level4(DATA, LEVEL_FOUR_AVAILABLE_TOWERS)
        game_over = CampaignModeGameOverCondition()
    elif mode == "level5":
        level = Level5(DATA, LEVEL_FOUR_AVAILABLE_TOWERS)
        game_over = CampaignModeGameOverCondition()
    else:
<<<<<<< HEAD
        level = CampaignMode(DATA, LEVEL_THREE_AVAILABLE_TOWERS)
=======
        level = Level1(DATA, LEVEL_ONE_AVAILABLE_TOWERS)
>>>>>>> refs/remotes/origin/main
        game_over = CampaignModeGameOverCondition()

    model = GameModel(level, game_over, NoEnemiesRoundOverCondition(), shared_achievements)
    view = GameView(SCREEN_WIDTH, SCREEN_HEIGHT)
    controller = GameController(model, view)
    return Screen(model, view, controller)
