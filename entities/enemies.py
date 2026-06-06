from __future__ import annotations
from abc import ABC, abstractmethod
from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, FPS, DATA, ENEMY_COLORS
from random import choice

import pyxel


class EnemyState(ABC):
    @abstractmethod
    def start_tick(self, enemy: GenericEnemy) -> None: ...

    @abstractmethod
    def end_tick(self, enemy: GenericEnemy) -> None: ...

    @abstractmethod
    def receive_hit(self, enemy: GenericEnemy, damage: int) -> None: ...


class InactiveState(EnemyState):
    def start_tick(self, enemy):
        pass

    def end_tick(self, enemy):
        pass

    def receive_hit(self, enemy, damage):
        pass


class ActiveState(EnemyState):
    def start_tick(self, enemy):
        pass
    
    def end_tick(self, enemy):
        if not enemy.is_alive:
            enemy.set_state(InactiveState())
            return
        if enemy._path_index >= len(enemy._path) - 1:
            enemy.set_state(InactiveState())
            return # reached end of path

        # move toward next tile
        target_x, target_y = enemy._tile_to_screen(enemy._path[enemy._path_index + 1])
        dx = target_x - enemy._x_position
        dy = target_y - enemy._y_position
        dist = (dx ** 2 + dy ** 2) ** 0.5

        if DATA.get("smooth_movement", True):
            if dist <= enemy._current_speed:
                # snap to next tile
                enemy._x_position, enemy._y_position = target_x, target_y
                enemy._path_index += 1
            else:
                enemy._x_position += enemy._current_speed * dx / dist
                enemy._y_position += enemy._current_speed * dy / dist
        else:
            enemy._tick_counter += 1
            if enemy._tick_counter >= 2 * FPS:
                enemy._x_position, enemy._y_position = target_x, target_y
                enemy._path_index += 1
                enemy._tick_counter = 0

    def receive_hit(self, enemy, damage):
        enemy._hit_points -= damage
        if not enemy.is_alive:
            enemy.set_state(InactiveState())


#class HitState(EnemyState):
#    def start_tick(self, enemy):
#        enemy.set_state(ActiveState())
    
#    def end_tick(self, enemy):
#        if not enemy.is_alive:
#            enemy.set_state(InactiveState())

#    def receive_hit(self, enemy, damage):
#        enemy._hit_points -= damage


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
    def colors(self) -> list[int]: ...

    @property
    @abstractmethod
    def base_position(self) -> tuple[float, float]: ...

    @property
    @abstractmethod
    def position(self) -> tuple[float, float]: ...

    @property
    @abstractmethod
    def state(self) -> EnemyState: ...


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
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__()
        self._path = path
        self._path_index = 0
        self._hit_points = self.base_hit_points
        self._current_speed = self.base_speed * speed_multiplier
        # start at first tile of path
        self._x_position, self._y_position = self._tile_to_screen(path[0])
        self._tick_counter = 0
        self._colors = [2]
        self._state: EnemyState = ActiveState()
    
    def set_state(self, state: EnemyState) -> None:
        self._state = state

    @property
    def grid_position(self):
        return self._path[self._path_index]
    
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
    def colors(self):
        return self._colors

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
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )

    @property
    def base_speed(self) -> int:
        return TILE_SIDE_LENGTH / (0.5 * FPS)  # 1 tile per 2 seconds

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

    @property
    def state(self) -> EnemyState:
        return self._state

    def receive_hit(self, damage: int) -> None:
        self._state.receive_hit(self, damage)

    def start_tick(self) -> None:
        self._state.start_tick(self)

    def end_tick(self) -> None:
        self._state.end_tick(self)


class Ube(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)


class Kutsinta(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)
        self._colors = [9]

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
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )


class Gulaman(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)
        self._colors = [11]

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            0, 32,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )


class Palitaw(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)
        self._colors = [7]

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            0, 64,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )

class Lecheflan(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)
        self._colors = [10]

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            32, 32,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )


class Champorado(GenericEnemy):
    def __init__(self, path, speed_multiplier = 1.0):
        super().__init__(path, speed_multiplier=speed_multiplier)
        self._colors = [4]

    # @property
    # def colors(self):
    #     return 4

    # diff
    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            32, 64,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )


class Regenerator(GenericEnemy):
    def __init__(self, *args, speed_multiplier = 1.0, regen_interval: int = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._regen_interval = regen_interval if regen_interval is not None else DATA.get("regenerator_interval", 3)
        self._cells_moved = 0
        self._last_path_index = 0  
        self._colors = ENEMY_COLORS

    def end_tick(self):
        super().end_tick()
        if self._path_index > self._last_path_index:
            cells_advanced = self._path_index - self._last_path_index
            self._cells_moved += cells_advanced
            if self._cells_moved % self._regen_interval == 0:
                self._hit_points += 1 
        self._last_path_index = self._path_index

    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            0, 160,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )

class Chameleon(GenericEnemy):
    def __init__(self, *args, speed_multiplier = 1.0, chameleon_interval: int = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._chameleon_interval = FPS * (chameleon_interval if chameleon_interval is not None else DATA.get("chameleon_interval", 60))
        self._ticks_since_colors_change = 0

    def end_tick(self):
        super().end_tick()
        if not self.is_alive:
            return
        self._ticks_since_colors_change += 1
        self._handle_change_colors()

    def _handle_change_colors(self):
        if self._ticks_since_colors_change >= self._chameleon_interval:
            self._change_colors()
            self._ticks_since_colors_change = 0

    def _change_colors(self):
        available = [c for c in ENEMY_COLORS if not (c in self._colors)]
        self._colors = [choice(available)]

    def draw(self, in_tunnel: bool = False):
        if in_tunnel:
            return
        sx, sy = self.get_sprite()
        x, y = self.position
        pyxel.blt(
            x - 16, y - 16,  # center the sprite
            0,               # image bank 0
            sx, sy,            # sprite starts at (0, 0)
            32, 32,          # 32x32
            0,                # transparent colors (black)
            scale=TILE_SIDE_LENGTH/32
        )

    def get_sprite(self):
        pairs = [
        (0, 96), (32, 96), (64, 96),
        (0, 128), (32, 128), (64, 128)
        ]
        for i, col in enumerate([2, 9, 11, 10, 7, 4]):
            if col in self._colors:
                return pairs[i]