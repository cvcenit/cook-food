from __future__ import annotations
from entities import Chef, Ube

class GameModel:
    def __init__(self, data: dict):
        self.lives = data["remaining_lives"]
        self.number_of_enemies = data["remaining_enemies"]
        self.rounds = 12
        self.damage = 1
        self.enemies = [Ube(1) for _ in range(self.number_of_enemies)]
        self._is_game_over = False
        self._current_tick = 1
        #self.player = player

    def update(self):
        if not self._is_game_over:
            self._current_tick += 1
            for enemy in self.enemies:
                enemy.end_tick()