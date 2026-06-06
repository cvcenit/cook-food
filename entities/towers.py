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


class BulletState(ABC):
    @abstractmethod
    def end_tick(self, bullet: Bullet) -> None: ...

    @abstractmethod
    def on_shoot(self, bullet: Bullet) -> None: ...

    @property
    @abstractmethod
    def is_active(self) -> bool: ...


class InactiveState(BulletState):
    def end_tick(self, bullet):
        pass

    def on_shoot(self, bullet):
        pass

    @property
    def is_active(self) -> bool:
        return False


class ReadiedState(BulletState):
    def end_tick(self, bullet):
        pass

    def on_shoot(self, bullet):
        bullet.set_state(FlightState())
    
    @property
    def is_active(self) -> bool:
        return True


class FlightState(BulletState):
    def end_tick(self, bullet):
        bullet.apply_velocity()
        if bullet.is_out_of_screen():
            bullet.set_state(InactiveState())

    def on_shoot(self, bullet):
        pass
    
    @property
    def is_active(self) -> bool:
        return True


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


class GenericBullet(BulletInfo):
    def __init__(self, col, r, initial_pos, initial_vel):
        # Base values
        self._base_velocity = initial_vel
        self._base_position = initial_pos
        self._color = col
        self._radius = r
        self._damage = 1 # HP
        self._is_active = False
        self._craters = []

        # Current values
        self._current_position = self.base_position
        self._current_velocity = self.base_velocity
        self._state: BulletState = ReadiedState()

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
        return self._state.is_active

    def change_velocity(self, vel):
        self._current_velocity = vel

    def change_position(self, pos):
        self._current_position = pos

    def change_radius(self, rad):
        self._radius = rad
    
    def set_radius_scale(self, scale: float):
        self._radius = BULLET_RADIUS * scale

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
        self.set_state(InactiveState())

    def collide_with(self, enemy):
        if self.color in enemy.colors:
            half_tile = TILE_SIDE_LENGTH / 2
            ex, ey = enemy.position
            bx, by = self.current_position
            px = max((ex - half_tile), min(bx, ex + half_tile))
            py = max((ey - half_tile), min(by, ey + half_tile))

            distance_square = (bx - px) ** 2 + (by - py) ** 2
            if distance_square <= self.radius ** 2:
                enemy.receive_hit(1)
                self.deactivate()
                return True
        return False

    def draw_bullet(self):
        (x, y), r = self.current_position, self.radius
        pyxel.circ(x, y, r, self.color)

    def process_enemies(self, enemies):
        ...

    def affect_nearby_enemies(self, enemies):
        ...

    def start_tick(self):
        ...

    def end_tick(self):
        self._state.end_tick(self)
    
    def on_shoot(self):
        self._state.on_shoot(self)
    
    def set_state(self, state: BulletState) -> None:
        self._state = state

    @property
    def craters(self):
        return self._craters
    

class Bullet(GenericBullet):
    def __init__(self, col, r, initial_pos, initial_vel):
        super().__init__(col, r, initial_pos, initial_vel)

class PiercingBullet(GenericBullet):
    def __init__(self, col, r, initial_pos, initial_vel, collision_amount):
        super().__init__(col, r, initial_pos, initial_vel)
        self._remaining_collision_amount = collision_amount

    @property
    def remaining_collision_amount(self):
        return self._remaining_collision_amount

    def collide_with(self, enemy):
        if self.remaining_collision_amount > 0:
            if self.color in enemy.colors:
                self._remaining_collision_amount -= 1
                half_tile = TILE_SIDE_LENGTH / 2
                ex, ey = enemy.position
                bx, by = self.current_position
                px = max((ex - half_tile), min(bx, ex + half_tile))
                py = max((ey - half_tile), min(by, ey + half_tile))

                distance_square = (bx - px) ** 2 + (by - py) ** 2
                if distance_square <= self.radius ** 2:
                    enemy.receive_hit(1)
                    return True
        return False

    def end_tick(self):
        if self._remaining_collision_amount <= 0:
            self.deactivate()
        super().end_tick()

class HomingBullet(GenericBullet):
    def __init__(self, col, r, initial_pos, initial_vel):
        super().__init__(col, r, initial_pos, initial_vel)
        self._nearest_enemy = None
        self._last_direction = None

    def process_enemies(self, enemies):
        nearest_e = None

        half_tile = TILE_SIDE_LENGTH / 2
        bx, by = self.current_position

        for i, enemy in enumerate(enemies):
            ex, ey = enemy.position
            px = max((ex - half_tile), min(bx, ex + half_tile))
            py = max((ey - half_tile), min(by, ey + half_tile))

            distance_square = (bx - px) ** 2 + (by - py) ** 2
            if i == 0:
                nearest_e = enemy
                nearest_dist = distance_square
            else:
                if distance_square < nearest_dist:
                    nearest_e = enemy
                    nearest_dist = distance_square

        self._nearest_enemy = nearest_e

    def generate_velocity_to_nearest_enemy(self):
        vel = 2 * BULLET_VELOCITY_MAGNITUDE
        if self._nearest_enemy is not None and self.color in self._nearest_enemy.colors:
                half_tile = TILE_SIDE_LENGTH / 2
                bx, by = self.current_position
                ex, ey = self._nearest_enemy.position
                px = max((ex - half_tile), min(bx, ex + half_tile))
                py = max((ey - half_tile), min(by, ey + half_tile))
                direction = atan2(by - ey, -bx + ex)
                self._last_direction = direction
        else:
            x, y = self.current_velocity
            self._last_direction = atan2(y, x)
        return vel * cos(self._last_direction), vel * sin(self._last_direction)

    def end_tick(self):
        if self._nearest_enemy is not None:
            self.change_velocity(self.generate_velocity_to_nearest_enemy())
        super().end_tick()

class ExplodingBullet(GenericBullet):
    def __init__(self, col, r, initial_pos, initial_vel):
        super().__init__(col, r, initial_pos, initial_vel)
        self._craters = []

    def collide_with(self, enemy):
        if super().collide_with(enemy):
            x, y = enemy.position

            enemy.receive_hit(1)
            self._craters += [(x, y),]

    def affect_nearby_enemies(self, enemies):
        for e in enemies:
            x, y = e.position

            e.receive_hit(1)
            self._craters += [(x, y),]

    def end_tick(self):
        print(self.craters)
        super().end_tick()

class PandesalBullet(HomingBullet, ExplodingBullet):
    def __init__(self, col, r, initial_pos, initial_vel):
        super().__init__(col, r, initial_pos, initial_vel)

class Tower(TowerInfo):
    def __init__(self, grid_position):
        self._grid_position = grid_position
        self._base_direction = PI / 2 # 90 degrees, "upwards"
        self._fire_rate = 0.5 # bullets per second
        self._purchase_cost = 5 # exp
        self._upgrade_costs = [0, 5] # exp

        self._bullet_type = Bullet
        self._bullet_amount = 1
        self._max_bullet_amount = 3

        self._radius = TILE_SIDE_LENGTH / 2.5
        self._craters = []
        self._crater_timer = 1

        self._bullets = []
        self._current_direction = self.base_direction
        self._color = 7
        self._remaining_seconds_to_shoot = self._fire_rate

        self._next_bullets = []

        self._tower_level = 1
        self._max_level = 2

    def __str__(self):
        return "Generic"

    @property
    def max_bullet_amount(self):
        return self._max_bullet_amount
    

    def change_fire_rate(self, fire_rate):
        self._fire_rate = fire_rate

    @property
    def bullet_amount(self):
        return self._bullet_amount
    
    def change_bullet_amount(self, amount):
        self._bullet_amount = amount

    @property
    def color(self):
        return self._color

    @property
    def max_level(self):
        return self._max_level
    
    @property
    def is_max_level(self):
        return self._max_level == self._tower_level

    @property
    def current_upgrade_cost(self):
        if len(self._upgrade_costs) > self._tower_level:
            return self._upgrade_costs[self._tower_level]
        return 0

    @property
    def craters(self):
        return self._craters

    @property
    def tower_level(self):
        return self._tower_level
    
    @property
    def purchase_cost(self):
        return self._purchase_cost

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
        if self._tower_level == self._max_level:
            return False
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        temp = min(self._max_level, self.tower_level + 1)
        self._tower_level = temp
        self._bullet_amount = temp
        return True

    def bullet_velocity(self, direction) -> tuple[float, float]:
        return BULLET_VELOCITY_MAGNITUDE * cos(direction), BULLET_VELOCITY_MAGNITUDE * sin(direction)

    def change_direction(self, direction) -> None:
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        cardinal_directions = (PI / 2, 0, 3 * PI / 2, PI)
        self._current_direction = cardinal_directions[direction]

    @property
    def next_bullets(self):
        return self._next_bullets

    def change_color(self, color):
        self._color = color

    def next_bullet_color(self):
        colors = []
        for bullet in self._next_bullets:
            colors += [bullet.color]
        current = choice(ENEMY_COLORS)
        while current in colors:
            current = choice(ENEMY_COLORS)
        return current

    def next_bullet_position(self, bullet_index):
        bullets_are_odd = self._bullet_amount % 2
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
        if len(self._next_bullets) < self._bullet_amount:
            bullet_color = self.next_bullet_color()

            bullet = self._bullet_type(bullet_color, BULLET_RADIUS * self._radius_scale, self.next_bullet_position(bullet_index), (0, 0))

            self._bullets.append(bullet)
            self._next_bullets.append(bullet)

    def shoot(self):
        if self._next_bullets:
            if self.can_shoot:
                for bullet in self._next_bullets:
                    bullet.change_velocity(self.bullet_velocity(self.current_direction))
                    bullet.set_state(FlightState())
                self._remaining_seconds_to_shoot = 1 / self._fire_rate
                self._next_bullets = []

    def decrement_reload_time(self):
        self._remaining_seconds_to_shoot -= 1 / FPS

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.circ(x, y, self._radius, self.color)

    def _load_next_bullet(self):
        for i in range(self._bullet_amount):
            self.load_next_bullet(i)
    
    @property
    def _radius_scale(self) -> float:
        return (1 - (self._remaining_seconds_to_shoot * self._fire_rate))

    def _update_next_bullet_radius(self):
        for bullet in self._next_bullets:
            bullet.set_radius_scale(self._radius_scale)
            
    def end_tick(self):
        if self._craters:
            if self._crater_timer <= 0:
                self._craters = []
            else:
                self._crater_timer -= 1 / FPS
        else:
            self._crater_timer = 1
            self.get_craters()

        self._load_next_bullet()

        if self.can_shoot and self._remaining_seconds_to_shoot != 0:
            self._remaining_seconds_to_shoot = 0
            self.shoot()

        self.decrement_crater()
        self.decrement_reload_time()
        self.remove_inactive_bullets()
        self._update_next_bullet_radius()

    def remove_inactive_bullets(self):
        self._bullets = [bullet for bullet in self.bullets if bullet.is_active]

    def affect_nearby_towers(self, towers):
        ...

    def get_craters(self):
        res = []
        for bullet in self._bullets:
            res += bullet.craters
        self._craters = res

    def decrement_crater(self):
        self._crater_timer -= 1 / FPS

class Taho(Tower):
    def __init__(self, grid_position):
        super().__init__(grid_position)

    def __str__(self):
        return "Taho"

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.blt(
            x - 16,
            y - 16,
            1,
            96, 64,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
        )

class Ihaw(Tower):
    def __init__(self, grid_position):
        super().__init__(grid_position)
        self._bullet_type = PiercingBullet
        self._bullet_amount = 1
        self._piercing_amount = 1
        self._max_bullet_amount = 2

    def __str__(self):
        return "Ihaw"

    def upgrade_tower(self):
        if self._tower_level == self._max_level:
            return False
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        temp = min(self._max_level, self.tower_level + 1)
        self._tower_level = temp
        if self.tower_level == 2:
            self._piercing_amount = 999
        return True

    def load_next_bullet(self, bullet_index):
        if len(self._next_bullets) < self._tower_level:
            bullet_color = self.next_bullet_color()

            bullet = self._bullet_type(
            bullet_color, 
            BULLET_RADIUS * (1 - 1.9 * self._remaining_seconds_to_shoot), 
            self.next_bullet_position(bullet_index), 
            (0, 0),
            999 if self.is_max_level else 1
            )

            self._bullets.append(bullet)
            self._next_bullets.append(bullet)

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.blt(
            x - 16,
            y - 16,
            1,
            96, 96,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
        )

class Sorbetes(Tower):
    def __init__(self, grid_position):
        super().__init__(grid_position)
        self._purchase_cost = 10
        self._bullet_amount = 0
        self._upgrade_costs = [0, 10]

    def __str__(self):
        return "Sorbetes"

    def upgrade_tower(self):
        if self._tower_level == self._max_level:
            return False
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        temp = min(self._max_level, self.tower_level + 1)
        self._tower_level = temp
        return True

    def affect_nearby_towers(self, towers):
        if self.is_max_level:
            for t in towers:
                new_amount = min(t.max_bullet_amount, t.bullet_amount + 1)
                t.change_bullet_amount(new_amount)
            for t in towers:
                new_rate = min(4, 2 * t.fire_rate)
                t.change_fire_rate(new_rate)
        else:
            for t in towers:
                new_rate = min(3, 2 * t.fire_rate)
                t.change_fire_rate(new_rate)


    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.blt(
            x - 16,
            y - 16,
            1,
            96, 32,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
        )

class Pandesal(Tower):
    def __init__(self, grid_position):
        super().__init__(grid_position)
        self._purchase_cost = 10
        self._bullet_type = HomingBullet
        self._fire_rate = 2
        self._max_bullet_amount = 2
        self._upgrade_costs = [0, 5]

    def __str__(self):
        return "Pandesal"

    def upgrade_tower(self):
        if self._tower_level == self._max_level:
            return False
        for bullet in self._next_bullets:
            bullet.deactivate()
        self._next_bullets = []
        temp = min(self._max_level, self.tower_level + 1)
        self._tower_level = temp
        if self.tower_level == 2:
            self._bullet_type = PandesalBullet
        return True

    def bullet_velocity(self, direction):
        vel = 2 * BULLET_VELOCITY_MAGNITUDE
        return vel * cos(direction), vel * sin(direction)

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.blt(
            x - 16,
            y - 16,
            1,
            96, 128,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
        )

class Chef(Tower):
    def __init__(self, grid_position):
        super().__init__(grid_position)
        self._fire_rate = 0.9
        self._tower_level = 5

    def change_direction(self, direction) -> None:
        self._current_direction = direction
        for i, bullet in enumerate(self._next_bullets):
            bullet.change_position((self.next_bullet_position(i)))
    
    def end_tick(self):
        self._load_next_bullet()

        if self.can_shoot and self._remaining_seconds_to_shoot != 0:
            self._remaining_seconds_to_shoot = 0

        self.decrement_reload_time()
        self.remove_inactive_bullets()
        self._update_next_bullet_radius()

    def draw_tower(self):
        x, y = self.screen_position()
        pyxel.blt(
            x - 16,
            y - 16,
            1,
            96, 0,
            32, 32,
            0,
            scale=TILE_SIDE_LENGTH/32
        )
