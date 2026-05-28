from abc import ABC, abstractmethod
from utils import SCREEN_WIDTH, SCREEN_HEIGHT

class TowerInfo(ABC):
    ...

class BulletInfo(ABC):
    @property
    @abstractmethod
    def base_position(self) -> Tuple[float, float]:
        ...

    @property
    @abstractmethod
    def base_velocity(self) -> Tuple[float, float]:
        ...

    @property
    @abstractmethod
    def current_position(self) -> Tuple[float, float]:
        ...
    
    @property
    @abstractmethod
    def current_velocity(self) -> Tuple[float, float]:
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
        # Current values
        self._current_position = self.base_position
        self._current_velocity = self.base_velocity
        self._is_active = False

        # Base values
        self._base_velocity = initial_vel
        self._base_position = initial_pos
        self._color = col
        self._radius = r

    @property
    def base_position(self) -> Tuple[float, float]:
        return self._base_position

    @property
    def base_velocity(self) -> Tuple[float, float]:
        return self._base_velocity

    @property
    def current_position(self) -> Tuple[float, float]:
        return self._current_position
    
    @property
    def current_velocity(self) -> Tuple[float, float]:
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

    def is_out_of_screen(self) -> bool:
        (x, y), r = self.current_position, self.radius
        return (x - r >= SCREEN_WIDTH) or (y - r >= SCREEN_HEIGHT) or (y + r <= 0) or (x + r <= 0)

    def deactivate_self(self) -> None:
        self._is_active = False

class Tower(TowerInfo):
    def __init__(self):
        pass

class Chef(Tower):
    def __init__(self):
        pass