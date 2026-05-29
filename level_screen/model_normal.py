from __future__ import annotations
from entities.enemies import Ube
from entities.towers import Chef, Tower
from modes import Level, CampaignMode, GameOverCondition, RoundOverCondition
from graphics import TextButton


NORMAL_MODE_BUTTONS = [TextButton(48, 192, "Pause", 1),]

# part ni jowee
# TODO: Load level
# TODO: Load player
# TODO: Load grid

# part ko pa
# TODO: Separate UI Logic and Game Logic in an elegant manner
# TODO: Add collision
class GameLogic:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self._level = level
        self._round_index = 0

        self._exp = level.initial_exp
        self._lives = level.initial_lives
        self._load_round(self._round_index)

        #self.rounds = 12
        #self.enemies = [Ube(1) for _ in range(self.number_of_enemies)]
        #self.path = levelpath

        # player data
        #self._player = Chef(2, (8, 5)) # this will make sense after I create that chef class
        #self.lives = data["remaining_lives"]
        #self.damage = 1

        #self._towers = [Tower(2, (5, 5))]

        # game data
        self._is_game_over = False
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition

    def _load_round(self, index: int):
        round_config = self._level.rounds[index]

        self._path = round_config.path
        self._enemies = [factory(round_config.path) for factory in round_config.enemies]
        self._player = Chef(2, round_config.player_start)
        self._towers = []

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @property
    def player(self):
        return self._player

    @property
    def towers(self):
        return self._towers

    @property
    def enemies(self):
        return self._enemies

    @property
    def lives(self) -> int:
        return self._lives

    @property
    def exp(self) -> int:
        return self._exp

    @property
    def rounds_left(self) -> int:
        return len(self._level.rounds) - self._round_index

    @property
    def bullets(self):
        result = []
        for tower in self._towers:
            result += tower.bullets
        return result + self._player.bullets
    
    def place_tower(self, tower: Tower) -> bool:
        if self._exp >= tower._purchase_cost:
            self._exp -= tower._purchase_cost
            self._towers.append(tower)
            return True
        return False
    
    def defeat_enemy(self, enemy) -> None:
        enemy.receive_hit(999)
        self._exp += enemy.points
    
    def lose_life(self) -> None:
        self._lives -= 1

    def player_change_direction(self, direction):
        self._player.change_direction(direction)

    def player_shoot(self, direction):
        self._player.shoot(direction)

    def advance_round(self) -> None:
        self._round_index += 1
        if self._round_index < len(self._level.rounds):
            self._load_round(self._round_index)

    def update(self):
        if self._is_game_over:
            return
        
        for tower in self._towers:
            tower.end_tick()

        for bullet in self.bullets:
            bullet.end_tick()

        for enemy in self._enemies:
            enemy.end_tick()

        self._player.end_tick()

        for bullet in self.bullets:
            for enemy in self._active_enemies:
                ex, ey = enemy.position
                bx, by = bullet.current_position
                distance_square = (bx - ex) ** 2 + (by - ey) ** 2
                hit_distance = bullet.radius + 25
                if distance_square <= hit_distance ** 2:
                    self.defeat_enemy(enemy)
                    bullet.deactivate()
                    
        if self._round_over_condition.is_round_over(len(self._active_enemies)):
            self.advance_round()
        
        if self._game_over_condition.is_game_over(len(self._active_enemies), self._lives, self.rounds_left):
            self._is_game_over = True

    @property
    def _active_enemies(self):
        return [enemy for enemy in self._enemies if enemy.is_alive]

class GameModel:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self._current_tick = 1
        self._game_logic = GameLogic(level, game_over_condition, round_over_condition)

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
        if clicked_idx is not None:
            self.change_screen(self._states[clicked_idx])

        self._game_logic.update()
        self._current_tick += 1