from __future__ import annotations
from entities.enemies import Ube
from entities.chefs import Chef
from modes import GameOverCondition, RoundOverCondition
from graphics import TextButton

class GameModel:
    def __init__(self, data: dict, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        # LOGIC NG GAME MISMO
        self.lives = data["remaining_lives"]
        self.number_of_enemies = data["remaining_enemies"]
        self.rounds = 12
        self.damage = 1
        self.enemies = [Ube(1) for _ in range(self.number_of_enemies)]
        self._is_game_over = False
        self._current_tick = 1
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition
        self._player = 1 # this will make sense after I create that chef class
        #self.path = levelpath

        # UI STUFF
        self._buttons = [
        TextButton(48, 192, "Back", 1),
        ]
        self._is_current_screen = False
        self._states = ["main"]
        self._state = self.base_state

    @property
    def is_game_over(self):
        return self._is_game_over

    @property
    def buttons(self):
        return self._buttons

    @property
    def player(self):
        return self._player

    @property
    def is_current_screen(self):
        return self._is_current_screen
    
    @property
    def state(self):
        return self._state

    @property
    def current_tick(self):
        return self._current_tick

    @property
    def base_state(self):
        return "play"

    @property
    def active_bullets(self):
        # bullets will be objects as well, will put it in the entities tomorrow
        ...
    

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

    def change_screen(self, state):
        self._is_current_screen = False
        self._current_tick = 1
        self._state = state

    def start_screen(self):
        self._is_current_screen = True
        self._current_tick = 1
        self._state = "play"