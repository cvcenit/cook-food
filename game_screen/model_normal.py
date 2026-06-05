from __future__ import annotations
from achievements import AchievementManager
from entities.enemies import Ube
from entities.towers import Chef, Taho, Pandesal, Sorbetes, Ihaw
from leaderboards import register_player
from modes import Level, CampaignMode, GameOverCondition, RoundOverCondition
from graphics import TextButton, SpriteButton, SpriteInfo, TextGraphic, PopupScreen, TextInput
from utils import GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, TILE_SIDE_LENGTH, FPS, SCREEN_WIDTH, SCREEN_HEIGHT

import pyxel

LEVEL_ONE_AVAILABLE_TOWERS = [Taho,]
LEVEL_TWO_AVAILABLE_TOWERS = LEVEL_ONE_AVAILABLE_TOWERS + [Ihaw]
LEVEL_THREE_AVAILABLE_TOWERS = LEVEL_TWO_AVAILABLE_TOWERS + [Sorbetes]
LEVEL_FOUR_AVAILABLE_TOWERS = LEVEL_THREE_AVAILABLE_TOWERS + [Pandesal]

BUTTON_SPRITES = [
    SpriteInfo(1, (0, 0), (96, 32)),
    SpriteInfo(1, (0, 32), (96, 32)),
    SpriteInfo(1, (0, 64), (96, 32)),
    SpriteInfo(1, (0, 96), (96, 32)),
    SpriteInfo(1, (0, 128), (96, 32))
]
SIDEBAR_BUTTONS = [
    TextButton(90, 20, "Pause", 1, size=24),
    SpriteButton(140, 435, BUTTON_SPRITES[2], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 535, BUTTON_SPRITES[3], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 635, BUTTON_SPRITES[1], BUTTON_SPRITES[0], 240/96),
    SpriteButton(140, 735, BUTTON_SPRITES[4], BUTTON_SPRITES[0], 240/96)
    ]

SCREEN_CHANGE_BUTTONS = [
    TextButton(0, 325, "Back to menu", 6, size=48),
]

PAUSE_POPUP_BUTTONS = [
    SCREEN_CHANGE_BUTTONS[0],
    TextButton(0, 475, "Return to game", 6, size=60),
    TextButton(0, 375, "Restart level", 6, size=56)
]

PAUSE_POPUP_TEXTS = [
    TextGraphic(50, 175, "Paused", 6, size=96),
]

for button in PAUSE_POPUP_BUTTONS:
    button.toggle_active()
    x, y = button.current_position
    button.change_position(((SCREEN_WIDTH - button.width)/ 2), y)

for text in PAUSE_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)


TOWER_POPUP_BUTTONS = [
    TextButton(0, 375, "Set direction (WASD)", 6, size=48),
    TextButton(0, 425, "Upgrade", 6, size=48),
    TextButton(0, 475, "Cancel", 6, size=48)
]

TOWER_POPUP_TEXTS = [
    TextGraphic(0, 200, "Level 1 Tower at (0, 0)", 6, size=32)
]

for button in TOWER_POPUP_BUTTONS:
    button.toggle_active()
    x, y = button.current_position
    button.change_position(((SCREEN_WIDTH - button.width)/ 2), y)

for text in TOWER_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)

DIRECTION_POPUP_TEXTS = [
    TextGraphic(0, 150, "W", 6, size=128),
    TextGraphic(0, 250, "A", 6, size=128),
    TextGraphic(0, 400, "S", 6, size=128),
    TextGraphic(0, 250, "D", 6, size=128)
]

for text in DIRECTION_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)

x, y = DIRECTION_POPUP_TEXTS[1].current_position
DIRECTION_POPUP_TEXTS[1].change_position(x - 200, y)

x, y = DIRECTION_POPUP_TEXTS[3].current_position
DIRECTION_POPUP_TEXTS[3].change_position(x + 200, y)

#
GAME_OVER_POPUP_BUTTONS = [
    SCREEN_CHANGE_BUTTONS[0],
    TextButton(0, 375, "Restart level", 6, size=56),
    TextButton(0, 475, "Register: ", 6, size=24),
]

GAME_OVER_POPUP_TEXTS = [
    TextGraphic(50, 175, "Game over!", 6, size=96),
    TextInput(0, 500, 6, size=24)
]

for button in GAME_OVER_POPUP_BUTTONS[1:]:
    button.toggle_active()
    x, y = button.current_position
    button.change_position(((SCREEN_WIDTH - button.width)/ 2), y)

for text in GAME_OVER_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)

WIN_POPUP_BUTTONS = [
    TextButton(0, 325, "Back to menu", 6, size=48),
    TextButton(0, 375, "Restart level", 6, size=56),
    TextButton(0, 475, "Register: ", 6, size=24),
]

WIN_POPUP_TEXTS = [
    TextGraphic(50, 175, "You Win!", 10, size=96),
    TextInput(0, 500, 6, size=24)
]
for button in WIN_POPUP_BUTTONS:
    button.toggle_active()
    x, y = button.current_position
    button.change_position(((SCREEN_WIDTH - button.width) / 2), y)
for text in WIN_POPUP_TEXTS:
    text.toggle_active()
    x, y = text.current_position
    text.change_position(((SCREEN_WIDTH - text.width) / 2), y)

pause_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, PAUSE_POPUP_BUTTONS, PAUSE_POPUP_TEXTS, 1)
tower_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, TOWER_POPUP_BUTTONS, TOWER_POPUP_TEXTS, 1)
direction_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, [], DIRECTION_POPUP_TEXTS, 1)
game_over_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, GAME_OVER_POPUP_BUTTONS, GAME_OVER_POPUP_TEXTS, 1)
win_popup = PopupScreen(SCREEN_WIDTH / 4, SCREEN_HEIGHT / 4, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, WIN_POPUP_BUTTONS, WIN_POPUP_TEXTS, 1)

class GameLogic:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition, achievements: AchievementManager):
        self._level = level
        self._round_index = 0

        self._exp = level.initial_exp
        self._lives = level.initial_lives
        self._load_round(self._round_index)
        self._placing_tower = False
        self._not_enough_exp = False
        self._towers = []
        self._available_towers = self._level.available_towers
        self._selected_tower_type = None

        self._selected_tower = None        

        # game data
        self._is_game_over = False
        self._is_game_won = False
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition

        self._achievements = achievements
        self._game_started = False
        self._achievement_display_timer = 0
        self._current_achievement_display = None

    def _load_round(self, index: int):
        round_config = self._level.get_round(index)
        self._paths = round_config.paths
        self._path = round_config.paths[0]
        self._grid = round_config.grid
        self._enemy_factories = round_config.enemies
        self._spawn_queue = list(round_config.enemies)
        self._spawn_interval = 2 * FPS
        self._spawn_timer = 0
        self._enemies = [] # [factory(round_config.path) for factory in round_config.enemies]
        self._player = Chef(round_config.player_start)
        self._tunnels = set(round_config.tunnels or [])

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    def change_selected_tower(self, tower):
        self._selected_tower = tower

    @property
    def selected_tower(self):
        return self._selected_tower
    
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
    def round_index(self) -> int:
        return self._round_index
    
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
    def achievements(self):
        return self._achievements
    
    @property
    def is_game_won(self) -> bool:
        return self._is_game_won

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
        for factory, path in self._spawn_queue:
            res.add(factory(path).color)
        return list(res)

    def toggle_placement_mode(self, tower_idx):
        self._placing_tower = not self.placing_tower
        if not self._placing_tower:
            self._not_enough_exp = False
        if self._placing_tower:
            self._selected_tower_type = self._available_towers[tower_idx]
        else:
            self._selected_tower_type = None

    def place_tower(self, mouse_x: float, mouse_y: float):
        # should not be instant (maybe add a timer)
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

        t = self._selected_tower_type((row, col))
        # should depend on the tower cost
        if self._exp >= t.purchase_cost:
            self._exp -= t.purchase_cost
            self._towers.append(t)
            self._placing_tower = False
            self._not_enough_exp = False # bug, spending doesnt mean not enough exp
            self._achievements.on_tower_placed()
        else:
            self._not_enough_exp = True

    def defeat_enemy(self, enemy) -> None:
        enemy.receive_hit(enemy.hit_points) 
        self._exp += enemy.points
        pyxel.play(1, 1)

    def lose_life(self) -> None:
        self._lives -= 1
        self._lives_lost_this_round = True

    def player_change_direction(self, direction):
        self._player.change_direction(direction)

    def player_shoot(self):
        self._player.shoot()

    def advance_round(self) -> None:
        self._achievements.on_round_complete()
        self._round_index += 1
        if self._round_index < len(self._level.rounds):
            self._load_round(self._round_index)
        else:
            self._is_game_won = True
            self._is_game_over = True

    def update(self):
        if self._is_game_over:
            return
        
        # SPAWNING INTERVAL FOR ENEMIES SO THAT THEY DO NOT STACK
        if self._spawn_queue:
            self._spawn_timer += 1
            if self._spawn_timer >= self._spawn_interval:
                factory, path = self._spawn_queue.pop(0)
                self._enemies.append(factory(path))
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
                    enemy_tile = enemy._path[enemy._path_index]
                    if enemy_tile in self._tunnels:
                        continue
                    ex, ey = enemy.position
                    bx, by = bullet.current_position
                    # fix, collision between square and circle
                    distance_square = (bx - ex) ** 2 + (by - ey) ** 2
                    hit_distance = bullet.radius + 25
                    if distance_square <= hit_distance ** 2:
                        enemy.receive_hit(1)
                        bullet.deactivate()
                        if not enemy.is_alive:
                            self._exp += enemy.points
                            self._achievements.on_enemy_killed()
                            pyxel.play(1, 1)
        
        for enemy in self._active_enemies:
            if enemy._path_index >= len(enemy._path) - 1:
                self.lose_life()
                enemy.receive_hit(999)
        
        # CHANGED TO NOT SELF._SPAWN_QUEUE TO SEE IF THERE ARE NO MORE ENEMIES IN THE QUEUE
        if not self._spawn_queue and self._round_over_condition.is_round_over(len(self._active_enemies)):
            self.advance_round()
        
        if self._game_over_condition.is_game_over(len(self._active_enemies), self._lives, self.rounds_left):
            self._is_game_over = True
            pyxel.play(2, 2)
        
        if self._achievements.unlocked and self._current_achievement_display is None:
            self._current_achievement_display = self._achievements.pop_unlocked()
            self._achievement_display_timer = 5 * FPS  # show for 5 seconds

        if self._current_achievement_display:
            self._achievement_display_timer -= 1
            if self._achievement_display_timer <= 0:
                self._current_achievement_display = None

        if not self._game_started:
            self._game_started = True
            self._achievements.on_game_start()

    def decrement_exp(self, de):
        self._exp -= de
    
    @property
    def _active_enemies(self):
        return [enemy for enemy in self._enemies if enemy.is_alive]

    @property
    def current_achievement_display(self):
        return self._current_achievement_display

class GameModel:
    def __init__(self, level: Level, game_over_condition: GameOverCondition, round_over_condition: RoundOverCondition, achievements: AchievementManager):
        self._current_tick = 1
        self._level = level
        self._game_over_condition = game_over_condition
        self._round_over_condition = round_over_condition
        self._achievements = achievements
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition, self._achievements)

        self._screen_change_buttons = SCREEN_CHANGE_BUTTONS

        self._popup_buttons = PAUSE_POPUP_BUTTONS + TOWER_POPUP_BUTTONS + GAME_OVER_POPUP_BUTTONS + WIN_POPUP_BUTTONS

        self._sidebar_buttons = list(SIDEBAR_BUTTONS)
        self._popup_screens = [pause_popup, tower_popup, direction_popup, game_over_popup, win_popup]
        self._is_paused = False
        self._register_message = None

        while len(self._sidebar_buttons) - 1 > len(self.game_logic._available_towers):
            self._sidebar_buttons.pop()

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
    
    @property
    def register_message(self):
        return self._register_message
    
    def handle_register(self, popup_idx: int, mode: str):
        name = self.popup_screens[popup_idx].texts[1]._text
        self._register_message = register_player(name, self._game_logic.round_index, mode)

    def toggle_pause(self):
        self._is_paused = not self._is_paused
        self.popup_screens[0].toggle_active()

    def start_screen(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition, self._achievements)
        for screen in self.popup_screens:
            if screen.is_active:
                screen.toggle_active()

    def reset(self):
        self._current_tick = 1
        self._game_logic = GameLogic(self._level, self._game_over_condition, self._round_over_condition, self._achievements)
        if self._is_paused:
            self.toggle_pause()
        for screen in self.popup_screens:
            if screen.is_active:
                screen.toggle_active()
        self._register_message = None

    def update_game_over(self):
        if self._game_logic.is_game_won:
            win_popup = self.popup_screens[4]
            if not win_popup.is_active:
                win_popup.toggle_active()
            input_text = win_popup.texts[1]
            input_text.listen()
            _, y = input_text.current_position
            input_text.change_position(((SCREEN_WIDTH - input_text.width) / 2), y)
        else:
            game_over_popup = self.popup_screens[3]
            if not game_over_popup.is_active:
                game_over_popup.toggle_active()
            input_text = game_over_popup.texts[1]
            input_text.listen()
            _, y = input_text.current_position
            input_text.change_position(((SCREEN_WIDTH - input_text.width)/ 2), y)
            
    def update_from_pause_menu(self, clicked_idx):
        if clicked_idx is not None:
            if clicked_idx == 1:
                self.toggle_pause()
            elif clicked_idx == 2:
                self.reset()
            else:
                ...

    def update_from_direction_menu(self, d):
        if d is not None:
            direction = d.lower()
            if self.game_logic.selected_tower is not None:
                yo = {"w": 0, "d": 1, "s": 2, "a": 3}
                self.game_logic.selected_tower.change_direction(yo.get(direction, 0))
            self.game_logic.change_selected_tower(None)
            if self.popup_screens[2].is_active:
                self.popup_screens[2].toggle_active()

    def update_from_tower_menu(self, clicked_idx):
        if clicked_idx is not None:
            t = self.game_logic.selected_tower
            if t is not None:
                match clicked_idx:
                    case 0:
                        # change direction
                        self.popup_screens[2].toggle_active()
                        self.popup_screens[1].toggle_active()
                    case 1:
                        cost = t.current_upgrade_cost
                        if self.game_logic.exp >= cost:
                            if t.upgrade_tower():
                                self.game_logic.decrement_exp(cost)
                        self._helper_update(self.game_logic.selected_tower)
                    case 2:
                        if self.popup_screens[2].is_active:
                            self.popup_screens[2].toggle_active()
                        self.popup_screens[1].toggle_active()
                    case _:
                        ...

    def update_towers(self, clicked_idx):
        if clicked_idx is not None:
            tower_selected = self.game_logic.towers[clicked_idx]
            self._helper_update(tower_selected)

    def _helper_update(self, tower_selected):
        self.game_logic.change_selected_tower(tower_selected)
        x, y = tower_selected.grid_position
        screen = self.popup_screens[1]
        text = screen.texts[0]
        text.change_text(f"Level {tower_selected.tower_level} Type Tower at ({x - 1}, {y})")
        x, y = screen.buttons[1].current_position
        if tower_selected.is_max_level:
            screen.buttons[1].change_text(f"Max Level (LVL{tower_selected.max_level})")
        else:
            screen.buttons[1].change_text(f"Upgrade: {tower_selected.current_upgrade_cost} EXP")
        screen.buttons[1].change_position(((SCREEN_WIDTH - screen.buttons[1].width)/ 2), y)
        x, y = text.current_position
        text.change_position(((SCREEN_WIDTH - text.width)/ 2), y)
        if not screen.is_active:
            screen.toggle_active()
    
    def update_from_sidebar(self, clicked_idx):
        if clicked_idx is not None:
            if clicked_idx == 0:
                self.toggle_pause()
            else:
                # has to know which tower
                self.game_logic.toggle_placement_mode(clicked_idx - 1)

    def update(self, clicked_idx):
        if self._is_paused:
            return
        self._current_tick += 1
        self.game_logic.update()
