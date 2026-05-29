from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from entities.enemies import Ube


@dataclass
class RoundConfig:
	enemies: list # list of callables
	path: list
	player_start: tuple

class Level(ABC):
	@property
	@abstractmethod
	def rounds(self) -> list[RoundConfig]:
		...
	
	@property
	@abstractmethod
	def initial_lives(self) -> int:
		...

	@property
	@abstractmethod
	def initial_exp(self) -> int:
		...

class CampaignMode(Level):
	def __init__(self, data: dict):
		path = [(5, col) for col in range(10)]
		enemy_count = data["remaining_enemies"]

		self._rounds = [
			RoundConfig(
				enemies=[lambda p: Ube(p) for _ in range(enemy_count)],
				path=path,
				player_start=(8,5),
			),
			RoundConfig(
				enemies=[lambda p: Ube(p) for _ in range(enemy_count + 2)],
				path=path,
				player_start=(8, 5),
			)
		]
		self._initial_lives = data["remaining_lives"]
	
	@property
	def rounds(self) -> list[RoundConfig]:
		return self._rounds
	
	@property
	def initial_lives(self) -> int:
		return self._initial_lives
	
	@property
	def initial_exp(self) -> int:
		return 0

class EndlessMode(Level):
	def __init__(self, data: dict):
		self._base_count = data["remaining_enemies"]
		self._initial_lives = data["remaining_lives"]
		self._path = [(5, col) for col in range(10)]
		
	def get_round(self, round_num: int) -> RoundConfig:
		count = self._base_count + round_num + 2
		return RoundConfig(
			enemies=[lambda p: Ube(p) for _ in range(count)],
			path=self._path,
			player_start=(8, 5),
		)
	
	@property
	def rounds(self) -> list[RoundConfig]:
		return []
	
	@property
	def initial_lives(self) -> int:
		return self._initial_lives
	
	@property
	def initial_exp(self) -> int:
		return 0


class GameOverCondition(ABC):
	@abstractmethod
	def is_game_over(self, enemies: int, lives: int, rounds: int) -> bool: 
		...

class RoundOverCondition(ABC):
	@abstractmethod
	def is_round_over(self, enemies: int) -> bool:
		...

class CampaignModeGameOverCondition(GameOverCondition):
	def is_game_over(self, enemies: int, lives: int, rounds: int) -> bool:
		return lives <= 0 or (enemies <= 0 and rounds <= 0)

class EndlessModeGameOverCondition(GameOverCondition):
	def is_game_over(self, enemies: int, lives: int, rounds: int) -> bool:
		return lives <= 0

class NoEnemiesRoundOverCondition(RoundOverCondition):
	def is_round_over(self, enemies: int) -> bool:
		return enemies <= 0
	
		