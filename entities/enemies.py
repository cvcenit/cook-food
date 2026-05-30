from abc import ABC, abstractmethod
from utils import TILE_SIDE_LENGTH, GAMEPLAY_X_OFFSET, GAMEPLAY_Y_OFFSET, FPS, DATA 

# entity types lang laman neto

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
    def sprite(self) -> int: ...

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

class Ube(Enemy):
    def __init__(self, path):
        super().__init__()
        self._path = path
        self._path_index = 0
        self._hit_points = self.base_hit_points
        self._current_speed = self.base_speed
        # start at first tile of path
        self._x_position, self._y_position = self._tile_to_screen(path[0])

    def _tile_to_screen(self, tile) -> tuple[float, float]:
        row, col = tile
        x = GAMEPLAY_X_OFFSET + col * TILE_SIDE_LENGTH + TILE_SIDE_LENGTH / 2
        y = GAMEPLAY_Y_OFFSET + row * TILE_SIDE_LENGTH + TILE_SIDE_LENGTH / 2
        return x, y

    @property
    def base_hit_points(self) -> int:
        return 1

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
    def color(self):
        return 2

    @property
    def sprite(self) -> int:
        return 2

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

        if dist <= self._current_speed:
            # snap to next tile
            self._x_position, self._y_position = target_x, target_y
            self._path_index += 1
        else:
            self._x_position += self._current_speed * dx / dist
            self._y_position += self._current_speed * dy / dist
        
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

class Chameleon(Enemy):
    pass