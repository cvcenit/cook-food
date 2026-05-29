from __future__ import annotations
from abc import ABC, abstractmethod
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_VELOCITY_MAGNITUDE, PI, TILE_SIDE_LENGTH, BULLET_RADIUS, FPS
from math import sin, cos
import pyxel

class TowerInfo(ABC):
    @property
    @abstractmethod
    def grid_position(self) -> tuple[int, int]:
        ...

    @property
    @abstractmethod
    def bullets(self) -> tuple[Bullet]:
        ...

class BulletInfo(ABC):
    @property
    @abstractmethod
    def base_position(self) -> tuple[float, float]:
        ...

    @property
    @abstractmethod
    def base_velocity(self) -> tuple[float, float]:
        ...

    @property
    @abstractmethod
    def current_position(self) -> tuple[float, float]:
        ...
    
    @property
    @abstractmethod
    def current_velocity(self) -> tuple[float, float]:
        ...

    @property
    @abstractmethod
    def color(self) -> int:
        ...

    @property
    @abstractmethod
    def radius(self) -> int:
        ...

    @property
    @abstractmethod
    def is_active(self) -> bool:
        ...

class Bullet(BulletInfo):
    def __init__(self, col, r, initial_pos, initial_vel):
        # Base values
        self._base_velocity = initial_vel
        self._base_position = initial_pos
        self._color = col
        self._radius = r
        self._damage = 1 # HP

        # Current values
        self._current_position = self.base_position
        self._current_velocity = self.base_velocity
        self._is_active = False

    @property
    def base_position(self) -> tuple[float, float]:
        return self._base_position

    @property
    def base_velocity(self) -> tuple[float, float]:
        return self._base_velocity

    @property
    def current_position(self) -> tuple[float, float]:
        return self._current_position
    
    @property
    def current_velocity(self) -> tuple[float, float]:
        return self._current_velocity

    @property
    def color(self) -> int:
        return self._color

    @property
    def radius(self) -> int:
        return self._radius

    @property
    def is_active(self) -> bool:
        return self._is_active

    def apply_velocity(self):
        vel_x, vel_y = self.current_velocity

        x, y = self._current_position
        x += vel_x
        y -= vel_y
        self._current_position = (x, y)

    def is_out_of_screen(self) -> bool:
        (x, y), r = self.current_position, self.radius
        return (x - r >= SCREEN_WIDTH) or (y - r >= SCREEN_HEIGHT) or (y + r <= 0) or (x + r <= 0)

    def deactivate(self) -> None:
        self._is_active = False

    def draw_bullet(self):
        (x, y), r = self.current_position, self.radius
        pyxel.circ(x, y, r, self.color)

    def initialize_bullet(self):
        self._is_active = True

    def start_tick(self):
        ...

    def end_tick(self):
        if self.is_active:
            self.apply_velocity()

        if self.is_out_of_screen():
            self.deactivate()

class Tower(TowerInfo):
    def __init__(self, color, grid_position):
        self._grid_position = grid_position
        self._base_direction = PI / 2 # 90 degrees, "upwards"
        self._fire_rate = 0.5 # bullets per second
        self._purchase_cost = 5 # exp
        self._upgrade_cost = 5 # exp

        self._bullets = []
        self._current_direction = self.base_direction
        self._color = color
        self._remaining_seconds_to_shoot = 0

    @property
    def color(self):
        return self._color

    @property
    def current_direction(self):
        return self._current_direction
    
    @property
    def base_direction(self):
        return self._base_direction

    @property
    def fire_rate(self):
        return self._fire_rate

    @property
    def grid_position(self):
        return self._grid_position

    @property
    def bullets(self):
        return self._bullets

    @property
    def can_shoot(self):
        return self._remaining_seconds_to_shoot <= 0
    
    def screen_position(self) -> tuple[float, float]:
        i, j = self.grid_position
        x_screen_offset = 0 # will change kapag finalized na
        y_screen_offset = 0 # will change kapag finalized na
        x = (j * TILE_SIDE_LENGTH) + x_screen_offset - (TILE_SIDE_LENGTH / 2)
        y = (i * TILE_SIDE_LENGTH) + y_screen_offset - (TILE_SIDE_LENGTH / 2)
        return x, y

    def bullet_velocity(self, direction) -> tuple[float, float]:
        return BULLET_VELOCITY_MAGNITUDE * cos(direction), BULLET_VELOCITY_MAGNITUDE * sin(direction)

    def change_direction(self, direction) -> None:
        cardinal_directions = (PI / 2, 0, 3 * PI / 2, PI)
        self._current_direction = cardinal_directions[direction]

    def change_color(self, color):
        self._color = color

    def shoot(self, direction):
        bullet = Bullet(self.color, BULLET_RADIUS, self.screen_position(), self.bullet_velocity(direction))
        bullet.initialize_bullet()
        self._bullets.append(bullet)
        self._remaining_seconds_to_shoot = self._fire_rate

    def decrement_reload_time(self):
        self._remaining_seconds_to_shoot -= self._fire_rate / FPS

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.circ(x, y, TILE_SIDE_LENGTH / 2, self.color)

    def end_tick(self):
        if self.can_shoot:
            self.shoot(self.current_direction)
        self.decrement_reload_time()
        self.remove_inactive_bullets()

    def remove_inactive_bullets(self):
        self._bullets = [bullet for bullet in self.bullets if bullet.is_active]

class Chef(Tower):
    def __init__(self, color, grid_position):
        super().__init__(color, grid_position)
        self._fire_rate = 0.9 # bullets per second

    def screen_position(self) -> tuple[float, float]:
        i, j = self.grid_position
        x_screen_offset = 0 # will change kapag finalized na
        y_screen_offset = 0 # will change kapag finalized na
        x = (j * TILE_SIDE_LENGTH) + x_screen_offset - (TILE_SIDE_LENGTH / 2)
        y = (i * TILE_SIDE_LENGTH) + y_screen_offset - (TILE_SIDE_LENGTH / 2)
        return SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2

    def change_direction(self, direction) -> None:
        self._current_direction = direction

    def change_color(self, color):
        self._color = color

    def shoot(self, direction):
        if self.can_shoot:
            bullet = Bullet(self.color, BULLET_RADIUS, self.screen_position(), self.bullet_velocity(direction))
            bullet.initialize_bullet()
            self._bullets.append(bullet)
            self._remaining_seconds_to_shoot = self._fire_rate

    def decrement_reload_time(self):
        self._remaining_seconds_to_shoot -= self._fire_rate / FPS

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.circ(x, y, TILE_SIDE_LENGTH / 2, self.color)

    def end_tick(self):
        self.decrement_reload_time()
        self.remove_inactive_bullets()
        print(self._remaining_seconds_to_shoot)

    def remove_inactive_bullets(self):
        self._bullets = [bullet for bullet in self.bullets if bullet.is_active]