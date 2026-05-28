from __future__ import annotations
from entities.enemies import Ube
from entities.towers import Chef, Tower
from modes import GameOverCondition, RoundOverCondition
from graphics import TextButton

# TODO: Separate UI Logic and Game Logic in an elegant manner

NORMAL_MODE_BUTTONS = [TextButton(48, 192, "Pause", 1),]

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
        self._player = Chef(2, (8, 5)) # this will make sense after I create that chef class
        self.lives = data["remaining_lives"]
        self.damage = 1

        self._towers = [Tower(2, (5, 5))]

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
    def towers(self):
        return self._towers

    @property
    def bullets(self):
        result = []
        tower_bullets = [b.bullets for b in self._towers]
        for bullet_list in tower_bullets:
            result += bullet_list
        return result + self._player.bullets 

class GameModel:
    def __init__(self, data: dict, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self._current_tick = 1
        self._game_logic = GameLogic(data, game_over_condition, round_over_condition)

        self._buttons = NORMAL_MODE_BUTTONS
        self._is_current_screen = False
        self._states = ["main"]
        self._state = self.base_state

    @property
    def current_tick(self):
        return self._current_tick

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

    def update(self, clicked_idx):
        if not self._game_logic._is_game_over:
            self._current_tick += 1
            if clicked_idx is not None:
                self.change_screen(self._states[clicked_idx])

            for tower in self._game_logic.towers:
                tower.end_tick()

            for bullet in self._game_logic.bullets:
                bullet.end_tick()

            for enemy in self._game_logic.enemies:
                enemy.end_tick()
        
            if self._game_logic._round_over_condition.is_round_over(self._game_logic.number_of_enemies):
                self._game_logic.rounds -= 1
            
            if self._game_logic._game_over_condition.is_game_over(self._game_logic.number_of_enemies, self._game_logic.lives, self._game_logic.rounds):
                self._game_logic._is_game_over = True
        else:
            # popup to level end screen
            ...