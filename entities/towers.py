from __future__ import annotations
from abc import ABC, abstractmethod
from utils import SCREEN_WIDTH, SCREEN_HEIGHT, BULLET_VELOCITY_MAGNITUDE, PI, TILE_SIDE_LENGTH, BULLET_RADIUS, FPS
from utils import GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, ENEMY_COLORS
from math import sin, cos, atan2, hypot
from random import choice
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

    def change_velocity(self, vel):
        self._current_velocity = vel

    def change_position(self, pos):
        self._current_position = pos

    def change_radius(self, rad):
        self._radius = rad

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

# TODO: Refactor, dapat maganda ung end_tick, i believe merong state kagaya ng moles 
# (towers ay may active, inactive state, depende sa current tick kung nagreload na ba)
# enemies, nasa kabilang file, meron ding hit state, active state, at inactive state
# lowkey, need neto dahil merong "readied state" ang bullet, different from "shot state", at "inactive state"

class Tower(TowerInfo):
    def __init__(self, color, grid_position):
        self._grid_position = grid_position
        self._base_direction = PI / 2 # 90 degrees, "upwards"
        self._fire_rate = 0.5 # bullets per second
        self._purchase_cost = 5 # exp
        self._upgrade_cost = 5 # exp

        self._radius = TILE_SIDE_LENGTH / 2.5

        self._bullets = []
        self._current_direction = self.base_direction
        self._color = color
        self._remaining_seconds_to_shoot = self._fire_rate

        self._next_bullets = []

        self._tower_level = 1
        self._max_level = 2

    @property
    def color(self):
        return self._color

    @property
    def tower_level(self):
        return self._tower_level
    
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

    def is_left_clicked(self) -> bool:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            if self.is_hovered():
                return True
        return False

    def is_right_clicked(self) -> bool:
        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
            if self.is_hovered():
                return True
        return False

    def is_hovered(self):
        x, y = self.screen_position()
        return x - self._radius <= pyxel.mouse_x <= x + self._radius and \
        y - self._radius <= pyxel.mouse_y <= y + self._radius
    
    def screen_position(self) -> tuple[float, float]:
        i, j = self.grid_position
        x_screen_offset = GAMEPLAY_X_OFFSET
        y_screen_offset = GAMEPLAY_Y_OFFSET
        x = (j * TILE_SIDE_LENGTH) + x_screen_offset + (TILE_SIDE_LENGTH / 2)
        y = (i * TILE_SIDE_LENGTH) + y_screen_offset + (TILE_SIDE_LENGTH / 2)
        return x, y

    def upgrade_tower(self):
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        temp = min(self._max_level, self.tower_level + 1)
        self._tower_level = temp

    def bullet_velocity(self, direction) -> tuple[float, float]:
        return BULLET_VELOCITY_MAGNITUDE * cos(direction), BULLET_VELOCITY_MAGNITUDE * sin(direction)

    def change_direction(self, direction) -> None:
        cardinal_directions = (PI / 2, 0, 3 * PI / 2, PI)
        self._current_direction = cardinal_directions[direction]

    @property
    def next_bullets(self):
        return self._next_bullets

    def change_color(self, color):
        self._color = color

    def next_bullet_color(self):
        return choice(ENEMY_COLORS)

    def next_bullet_position(self, bullet_index):
        bullets_are_odd = self._tower_level % 2
        bx, by = self.screen_position()
        theta = self.current_direction

        if bullets_are_odd:
            if bullet_index == 0:
                r = 0
            else:
                if bullet_index % 2:
                    r = - ((2 * bullet_index)) * (BULLET_RADIUS) - (BULLET_RADIUS * 2)
                else:
                    r = ((2 * (bullet_index - 1))) * (BULLET_RADIUS) + (BULLET_RADIUS * 2)
        else:
            if bullet_index % 2:
                r = - ((2 * bullet_index)) * (BULLET_RADIUS / 2) - (BULLET_RADIUS / 2)
            else:
                r = ((2 * (bullet_index + 1))) * (BULLET_RADIUS / 2) + (BULLET_RADIUS / 2)

        t = TILE_SIDE_LENGTH / 1.5
        beta = atan2(r, t)
        hyp = hypot(r, t)

        bx += (hyp) * cos(beta + theta)
        by -= (hyp) * sin(beta + theta)
        return bx, by

    def load_next_bullet(self, bullet_index):
        if len(self._next_bullets) < self._tower_level:
            bullet_color = self.next_bullet_color()

            bullet = Bullet(bullet_color, BULLET_RADIUS * (1 - 1.9 * self._remaining_seconds_to_shoot), self.next_bullet_position(bullet_index), (0, 0))

            bullet.initialize_bullet()
            self._bullets.append(bullet)
            self._next_bullets.append(bullet)

    def shoot(self):
        if self._next_bullets:
            if self.can_shoot:
                for bullet in self._next_bullets:
                    bullet.change_velocity(self.bullet_velocity(self.current_direction))
                self._remaining_seconds_to_shoot = self._fire_rate
                self._next_bullets = []

    def decrement_reload_time(self):
        self._remaining_seconds_to_shoot -= self._fire_rate / FPS

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.circ(x, y, self._radius, self.color)

    def end_tick(self):
        for i in range(self._tower_level):
            self.load_next_bullet(i)

        if self.can_shoot and self._remaining_seconds_to_shoot != 0:
            self._remaining_seconds_to_shoot = 0

        if self.can_shoot:
           self.shoot()

        self.decrement_reload_time()
        self.remove_inactive_bullets()

        for bullet in self._next_bullets:
            bullet.change_radius(BULLET_RADIUS * (1 - 1.9 * self._remaining_seconds_to_shoot))

    def remove_inactive_bullets(self):
        self._bullets = [bullet for bullet in self.bullets if bullet.is_active]

class Chef(Tower):
    def __init__(self, color, grid_position):
        super().__init__(color, grid_position)
        self._fire_rate = 0.9
        self._tower_level = 5

    def change_direction(self, direction) -> None:
        self._current_direction = direction
        for i, bullet in enumerate(self._next_bullets):
            bullet.change_position((self.next_bullet_position(i)))

    def end_tick(self):
        for i in range(self._tower_level):
            self.load_next_bullet(i)

        if self.can_shoot and self._remaining_seconds_to_shoot != 0:
            self._remaining_seconds_to_shoot = 0

        self.decrement_reload_time()
        self.remove_inactive_bullets()

        for bullet in self._next_bullets:
            bullet.change_radius(BULLET_RADIUS * (1 - self._remaining_seconds_to_shoot))