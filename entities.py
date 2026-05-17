from abc import ABC, abstractmethod

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
		self._hit_points = self.base_hit_points
		self._current_speed = self.base_speed
		self._x_position = self.base_position[0]
		self._y_position = self.base_position[1]
		self._path = path
		super().__init__()

	@property
	def base_hit_points(self) -> int:
		return 1

	@property
	def base_speed(self) -> int:
		return 2

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
		return self.hit_points > 0

	@property
	def sprite(self) -> int:
		return 2

	@property
	def base_position(self) -> tuple[float, float]:
		return (50, 50)

	@property
	def position(self) -> tuple[float, float]:
		return self._x_position, self._y_position

	def receive_hit(self, damage: int) -> None:
		self._hit_points -= damage

	def start_tick(self) -> None:
		...

	def end_tick(self) -> None:
		self._x_position += self.current_speed
		
#test this
class Chameleon(Enemy):
	pass

class Regenerator(Enemy):
	pass


class Tower(ABC):
	def __init__(self):
		pass


class Chef(ABC):
	def __init__(self):
		pass