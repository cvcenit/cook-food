from abc import ABC, abstractmethod
from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, FPS, DATA, ENEMY_COLORS
from random import choice

import pyxel

class EnemyInfo(ABC):
    @property
    @abstractmethod
    def base_hit_points(self) -> int: ...

    @property
    @abstractmethod
    def base_speed(self) -> int: ...

    @property
    @abstractmethod
    def current_speed(self) -> int: ...

    @property
    @abstractmethod
    def hit_points(self) -> int: ...

    @property
    @abstractmethod
    def points(self) -> int: ...

    @property
    @abstractmethod
    def is_alive(self) -> bool: ...

    @property
    @abstractmethod
    def color(self) -> int: ...

    @property
    @abstractmethod
    def base_position(self) -> tuple[float, float]: ...

    @property
    @abstractmethod
    def position(self) -> tuple[float, float]: ...

class Enemy(EnemyInfo):
    @abstractmethod
    def receive_hit(self, damage: int) -> None:
        ...

    @abstractmethod
    def start_tick(self) -> None:
        ...

    @abstractmethod
    def end_tick(self) -> None:
        ...

class GenericEnemy(Enemy):
    def __init__(self, path):
        super().__init__()
        self._path = path
        self._path_index = 0
        self._hit_points = self.base_hit_points
        self._current_speed = self.base_speed
        # start at first tile of path
        self._x_position, self._y_position = self._tile_to_screen(path[0])
        self._tick_counter = 0

    def _tile_to_screen(self, tile) -> tuple[float, float]:
        row, col = tile
        x = GAMEPLAY_X_OFFSET + col * TILE_SIDE_LENGTH + TILE_SIDE_LENGTH / 2
        y = GAMEPLAY_Y_OFFSET + row * TILE_SIDE_LENGTH + TILE_SIDE_LENGTH / 2
        return x, y

    # diff per enemy
    @property
    def base_hit_points(self) -> int:
        return 1

    # diff
    @property
    def color(self):
        return 2

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            0, 0,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0                # transparent color (black)
        )

    @property
    def base_speed(self) -> int:
        return TILE_SIDE_LENGTH / (2 * FPS)  # 1 tile per 2 seconds

    @property
    def current_speed(self) -> int:
        return self._current_speed

    @property
    def hit_points(self) -> int:
        return self._hit_points

    @property
    def points(self) -> int:
        return 1

    @property
    def is_alive(self) -> bool:
        return self._hit_points > 0

    @property
    def base_position(self) -> tuple[float, float]:
        return self._tile_to_screen(self._path[0])

    @property
    def position(self) -> tuple[float, float]:
        return self._x_position, self._y_position

    def receive_hit(self, damage: int) -> None:
        self._hit_points -= damage

    def start_tick(self) -> None:
        ...

    def end_tick(self) -> None:
        if not self.is_alive:
            return
        if self._path_index >= len(self._path) - 1:
            return  # reached end of path

        # move toward next tile
        target_x, target_y = self._tile_to_screen(self._path[self._path_index + 1])
        dx = target_x - self._x_position
        dy = target_y - self._y_position
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if DATA.get("smooth_movement", True):
            if dist <= self._current_speed:
                # snap to next tile
                self._x_position, self._y_position = target_x, target_y
                self._path_index += 1
            else:
                self._x_position += self._current_speed * dx / dist
                self._y_position += self._current_speed * dy / dist
        else:
            self._tick_counter += 1
            if self._tick_counter >= 2 * FPS:
                self._x_position, self._y_position = target_x, target_y
                self._path_index += 1
                self._tick_counter = 0

class Ube(GenericEnemy):
    def __init__(self, path):
        super().__init__(path)

class Kutsinta(GenericEnemy):
    def __init__(self, path):
        super().__init__(path)

    @property
    def base_hit_points(self) -> int:
        return 1

    @property
    def color(self):
        return 9

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            32, 0,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0                # transparent color (black)
        )


# refactor, mas maganda siguro kung may color nalang sila na argument
class RegeneratorMixin:
    def __init__(self, *args, regen_interval: int = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._regen_interval = regen_interval if regen_interval is not None else DATA.get("regenerator_interval", 3)
        self._cells_moved = 0
        self._last_path_index = 0  

    def end_tick(self):
        super().end_tick()
        if self._path_index > self._last_path_index:
            cells_advanced = self._path_index - self._last_path_index
            self._cells_moved += cells_advanced
            if self._cells_moved % self._regen_interval == 0:
                self._hit_points += 1 
        self._last_path_index = self._path_index

class RegeneratorUbe(RegeneratorMixin, Ube):
    def __init__(self, path, regen_interval: int = None):
        super().__init__(path, regen_interval=regen_interval)

class ChameleonMixin:
    def __init__(self, *args, chameleon_interval: int = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._chameleon_interval = chameleon_interval if chameleon_interval is not None else DATA.get("chameleon_interval", 60)
        self._ticks_since_color_change = 0

    def end_tick(self):
        super().end_tick()
        if not self.is_alive:
            return
        self._ticks_since_color_change += 1
        if self._ticks_since_color_change >= self._chameleon_interval:
            self._change_color()
            self._ticks_since_color_change = 0

    def _change_color(self):
        available = [c for c in ENEMY_COLORS if c != self._color]
        self._color = choice(available)

class ChameleonUbe(ChameleonMixin, Ube):
    def __init__(self, path, chameleon_interval: int = None):
        super().__init__(path, chameleon_interval=chameleon_interval)

class RegeneratorChameleonUbe(RegeneratorMixin, ChameleonMixin, Ube):
    def __init__(self, path, regen_interval=None, chameleon_interval=None):
        super().__init__(path, regen_interval=regen_interval, chameleon_interval=chameleon_interval)