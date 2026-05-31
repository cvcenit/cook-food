from __future__ import annotations
from entities.enemies import Ube
from entities.towers import Chef, Tower
from modes import Level, CampaignMode, GameOverCondition, RoundOverCondition
from graphics import TextButton
from utils import GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, TILE_SIDE_LENGTH, FPS


NORMAL_MODE_BUTTONS = [TextButton(48, 48, "Back", 1),]
SIDEBAR_BUTTONS = [TextButton(10, 192, "Tower 1", 1)]

# part ni jowee
# TODO: Load level
# TODO: Load player
# TODO: Load grid

class GameLogic:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self._level = level
        self._round_index = 0

        self._exp = level.initial_exp
        self._lives = level.initial_lives
        self._load_round(self._round_index)
        self._placing_tower = False
        self._not_enough_exp = False
        self._towers = []

        # game data
        self._is_game_over = False
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition

    def _load_round(self, index: int):
        round_config = self._level.rounds[index]
        self._path = round_config.path
        self._grid = round_config.grid
        self._enemy_factories = round_config.enemies
        self._spawn_queue = list(round_config.enemies)
        self._spawn_interval = 2 * FPS
        self._spawn_timer = 0
        self._enemies = [] # [factory(round_config.path) for factory in round_config.enemies]
        self._player = Chef(7, round_config.player_start)
        self._tunnels = set(round_config.tunnels or [])

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
    def grid(self):
        return self._grid
    
    @property
    def placing_tower(self) -> bool:
        return self._placing_tower
    
    @property
    def not_enough_exp(self) -> bool:
        return self._not_enough_exp

    @property
    def tunnels(self):
        return self._tunnels

    @property
    def bullets(self):
        result = []
        for tower in self._towers:
            result += tower.bullets
        return result + self._player.bullets

    def colors_of_remaining_enemies(self):
        res = set()
        for enemy in self._active_enemies:
            res.add(enemy.color)
        for enemy in self._spawn_queue:
            res.add(enemy(self._path).color)
        return list(res)
    
    def toggle_placement_mode(self):
        self._placing_tower = not self.placing_tower
        if not self._placing_tower:
            self._not_enough_exp = False

    def place_tower(self, mouse_x: float, mouse_y: float):
        col = int((mouse_x - GAMEPLAY_X_OFFSET) / TILE_SIDE_LENGTH)
        row = int((mouse_y - GAMEPLAY_Y_OFFSET) / TILE_SIDE_LENGTH)

        tiles = self._grid._tiles
        if not (0 <= row < len(tiles) and 0 <= col < len(tiles[0])):
            return
        if tiles[row][col]._isPath:
            return
        for tower in self._towers:
            if tower.grid_position == (row, col):
                return
        if self._exp >= 5:
            self._exp -= 5
            self._towers.append(Tower(2, (row, col)))
            self._placing_tower = False
            self._not_enough_exp = False
        else:
            self._not_enough_exp = True
    
    def defeat_enemy(self, enemy) -> None:
        enemy.receive_hit(enemy.hit_points) 
        self._exp += enemy.points
    
    def lose_life(self) -> None:
        self._lives -= 1

    def player_change_direction(self, direction):
        self._player.change_direction(direction)

    def player_shoot(self):
        self._player.shoot()

    def advance_round(self) -> None:
        self._round_index += 1
        if self._round_index < len(self._level.rounds):
            self._load_round(self._round_index)

    def update(self):
        if self._is_game_over:
            return
        
        # SPAWNING INTERVAL FOR ENEMIES SO THAT THEY DO NOT STACK
        if self._spawn_queue:
            self._spawn_timer += 1
            if self._spawn_timer >= self._spawn_interval:
                factory = self._spawn_queue.pop(0)
                self._enemies.append(factory(self._path))
                self._spawn_timer = 0

        for tower in self._towers:
            tower.end_tick(self._active_enemies)

        for bullet in self.bullets:
            bullet.end_tick()

        for enemy in self._enemies:
            enemy.end_tick()

        self._player.end_tick()

        active_bullets = [b for b in self.bullets if b.is_active]
        for bullet in active_bullets:
            for enemy in self._active_enemies:
                if not bullet.is_active:
                    continue
                bx, by = bullet.current_position
                for tunnel_tile in self._tunnels:
                    tr, tc, = tunnel_tile
                    tx = GAMEPLAY_X_OFFSET + tc * TILE_SIDE_LENGTH
                    ty = GAMEPLAY_Y_OFFSET + tr * TILE_SIDE_LENGTH
                    if tx <= bx <= tx + TILE_SIDE_LENGTH and ty <= by <= ty + TILE_SIDE_LENGTH:
                        bullet.deactivate()
                        break
                if not bullet.is_active:
                    continue
                if bullet.color == enemy.color:
                    ex, ey = enemy.position
                    enemy_tile = self._path[enemy._path_index]
                    if enemy_tile in self._tunnels:
                        continue
                    bx, by = bullet.current_position
                    distance_square = (bx - ex) ** 2 + (by - ey) ** 2
                    hit_distance = bullet.radius + 25
                    if distance_square <= hit_distance ** 2:
                        enemy.receive_hit(1)
                        bullet.deactivate()
                        if not enemy.is_alive:
                            self._exp += enemy.points
        
        for enemy in self._active_enemies:
            if enemy._path_index >= len(enemy._path) - 1:
                self.lose_life()
                enemy.receive_hit(999)
        
        # CHANGED TO NOT SELF._SPAWN_QUEUE TO SEE IF THERE ARE NO MORE ENEMIES IN THE QUEUE
        if not self._spawn_queue and self._round_over_condition.is_round_over(len(self._active_enemies)):
            self.advance_round()
        
        if self._game_over_condition.is_game_over(len(self._active_enemies), self._lives, self.rounds_left):
            self._is_game_over = True

        for enemy in self._active_enemies:
            if enemy._path_index >= len(enemy._path) - 1:
                self.lose_life()
                enemy.receive_hit(999)

    @property
    def _active_enemies(self):
        return [enemy for enemy in self._enemies if enemy.is_alive]

class GameModel:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition):
        self._current_tick = 1
        self._level = level
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition)

        self._screen_change_buttons = NORMAL_MODE_BUTTONS
        self._popup_buttons = []
        self._sidebar_buttons = SIDEBAR_BUTTONS

    @property
    def current_tick(self):
        return self._current_tick

    @property
    def screen_change_buttons(self):
        return self._screen_change_buttons

    @property
    def popup_buttons(self):
        return self._popup_buttons

    @property
    def sidebar_buttons(self):
        return self._sidebar_buttons

    def start_screen(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition)
        self._screen_change_buttons = NORMAL_MODE_BUTTONS

    def reset(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition)
        self._screen_change_buttons = NORMAL_MODE_BUTTONS

    def update(self, clicked_idx):
        self._game_logic.update()
        self._current_tick += 1