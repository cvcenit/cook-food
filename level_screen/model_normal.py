from __future__ import annotations
from entities.enemies import Ube
from entities.towers import Chef
from modes import GameOverCondition, RoundOverCondition
from graphics import TextButton

# TODO: Separate UI Logic and Game Logic in an elegant manner

NORMAL_MODE_BUTTONS = [TextButton(48, 192, "Pause", 1),]

# TODO: Add button for pause menu, and add the popup menu as well
class UILogic:
    def __init__(self):
        self._buttons = NORMAL_MODE_BUTTONS
        self._is_current_screen = False
        self._states = ["main"]
        self._state = self.base_state

    @property
    def buttons(self):
        return self._buttons

    @property
    def is_current_screen(self):
        return self._is_current_screen
    
    @property
    def state(self):
        return self._state

    @property
    def base_state(self):
        return "play"

    def change_screen(self, state):
        self._is_current_screen = False
        self._current_tick = 1
        self._state = state

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1
        self._state = "play"

# TODO: Load level
# TODO: Load player
# TODO: Load grid
# TODO: Add collision
# TODO: Add bullets
class GameLogic:
    def __init__(self, data: dict, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        # LOGIC NG GAME MISMO
        # data ay sa level na mismo

        # level data
        self.number_of_enemies = data["remaining_enemies"]
        self.rounds = 12
        self.enemies = [Ube(1) for _ in range(self.number_of_enemies)]
        #self.path = levelpath

        # player data
        self._player = 1 # this will make sense after I create that chef class
        self.lives = data["remaining_lives"]
        self.damage = 1

        # game data
        self._is_game_over = False
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition

    @property
    def is_game_over(self):
        return self._is_game_over

    @property
    def player(self):
        return self._player

    @property
    def active_bullets(self):
        # bullets will be objects as well, will put it in the entities tomorrow
        ...

class GameModel:
    def __init__(self):
        self._current_tick = 1

    @property
    def current_tick(self):
        return self._current_tick

    def update(self, clicked_idx):
        if not self._is_game_over:
            self._current_tick += 1
            if clicked_idx is not None:
                self.change_screen(self._states[clicked_idx])

            for enemy in self.enemies:
                enemy.end_tick()
        
            if self._round_over_condition.is_round_over(self.number_of_enemies):
                self.rounds -= 1
            
            if self._game_over_condition.is_game_over(self.number_of_enemies, self.lives, self.rounds):
                self._is_game_over = True
        else:
            # popup to level end screen
            ...