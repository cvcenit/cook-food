from __future__ import annotations
from entities.enemies import Ube
from entities.towers import Chef, Tower
from modes import Level, CampaignMode, GameOverCondition, RoundOverCondition
from graphics import TextButton, SpriteButton, SpriteInfo, TextGraphic, PopupScreen
from utils import GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, TILE_SIDE_LENGTH, FPS, SCREEN_WIDTH, SCREEN_HEIGHT


BUTTON_SPRITES = [
    SpriteInfo(1, (0, 0), (96, 32)),
    SpriteInfo(1, (0, 32), (96, 32)),
    SpriteInfo(1, (0, 64), (96, 32)),
    SpriteInfo(1, (0, 96), (96, 32))
]
SIDEBAR_BUTTONS = [
    TextButton(0, 0, "Pause", 1, size=24),
    SpriteButton(140, 435, BUTTON_SPRITES[0], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 535, BUTTON_SPRITES[1], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 635, BUTTON_SPRITES[2], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 735, BUTTON_SPRITES[3], BUTTON_SPRITES[0], 240/96)
    ]

SCREEN_CHANGE_BUTTONS = [
    TextButton(0, 325, "Back to menu", 6, size=48),
]

PAUSE_POPUP_BUTTONS = [
    SCREEN_CHANGE_BUTTONS[0],
    TextButton(0, 475, "Return to game", 6, size=60),
    TextButton(0, 375, "Restart level", 6, size=56)
]

for button in PAUSE_POPUP_BUTTONS:
    button.toggle_active()
    x, y = button.current_position
    button.change_position(((SCREEN_WIDTH - button.width)/ 2), y)

PAUSE_POPUP_TEXTS = [
    TextGraphic(50, 175, "Paused", 6, size=96),
]

for text in PAUSE_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)


pause_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PAUSE_POPUP_BUTTONS, PAUSE_POPUP_TEXTS, 1)
tower_popup = ...

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
        # should not be instant (pagkaselect ng tower, tinatry agad to, add a timer)
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

        # should depend on the tower cost
        if self._exp >= 5:
            self._exp -= 5
            self._towers.append(Tower(2, (row, col)))
            self._placing_tower = False
            self._not_enough_exp = False # dapat false lang kung exp < tower cost, hindi dahil nag spend false na
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
            tower.end_tick()

        for bullet in self.bullets:
            bullet.end_tick()

        for enemy in self._enemies:
            enemy.end_tick()

        self._player.end_tick()

        # pls refactor
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

                # enemy color will now be a list
                # will change to if bullet color in enemy colors
                # to account for regenerator (no color)
                if bullet.color == enemy.color:
                    enemy_tile = self._path[enemy._path_index]
                    if enemy_tile in self._tunnels:
                        continue
                    ex, ey = enemy.position
                    bx, by = bullet.current_position
                    # fix, dapat pag nagcollide na ung bullet sa square sasabog na
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

        self._screen_change_buttons = SCREEN_CHANGE_BUTTONS
        self._popup_buttons = PAUSE_POPUP_BUTTONS # add ung tower upgrade buttons later
        self._sidebar_buttons = SIDEBAR_BUTTONS

        self._popup_screens = [pause_popup]
        self._is_paused = False

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
    
    @property
    def is_paused(self):
        return self._is_paused
    
    @property
    def popup_screens(self):
        return self._popup_screens

    @property
    def game_logic(self):
        return self._game_logic

    def toggle_pause(self):
        self._is_paused = not self._is_paused
        self.popup_screens[0].toggle_active()

    def start_screen(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition)
        for screen in self.popup_screens:
            if screen.is_active:
                screen.toggle_active()

    def reset(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition)
        if self._is_paused:
            self.toggle_pause()
        for screen in self.popup_screens:
            if screen.is_active:
                screen.toggle_active()

    def update_from_pause_menu(self, clicked_idx):
        if clicked_idx == 1:
            self.toggle_pause()
        elif clicked_idx == 2:
            self.reset()
        else:
            ...

    def update_towers(self, clicked_idx):
        if clicked_idx is not None:
            self.game_logic.towers[clicked_idx].upgrade_tower()

    def update_from_sidebar(self, clicked_idx):
        if clicked_idx == 0:
            self.toggle_pause()
        else:
            # has to know which tower
            self.game_logic.toggle_placement_mode()

    def update(self, clicked_idx):
        if self._is_paused:
            return
        self._current_tick += 1
        self.game_logic.update()