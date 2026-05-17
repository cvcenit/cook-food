from __future__ import annotations
from entities import Chef, Ube
from modes import GameOverCondition, RoundOverCondition

class GameModel:
    def __init__(self, data: dict, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self.lives = data["remaining_lives"]
        self.number_of_enemies = data["remaining_enemies"]
        self.rounds = 12
        self.damage = 1
        self.enemies = [Ube(1) for _ in range(self.number_of_enemies)]
        self._is_game_over = False
        self._current_tick = 1
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition
        #self.player = player

    def update(self):
        if not self._is_game_over:
            self._current_tick += 1
            for enemy in self.enemies:
                enemy.end_tick()
        
        if self._round_over_condition.is_round_over(self.number_of_enemies):
            self.rounds -= 1
        
        if self._game_over_condition.is_game_over(self.number_of_enemies, self.lives, self.rounds):
            self._is_game_over = True

    def is_game_over(self):
        return self._is_game_over
    