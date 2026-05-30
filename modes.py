from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from entities.enemies import RegeneratorUbe, ChameleonUbe, RegeneratorChameleonUbe


@dataclass
class RoundConfig:
	enemies: list # list of callables
	path: list
	player_start: tuple

def make_spiral_path(rows=10, cols=10):
    path = []
    top, bottom, left, right = 0, rows - 1, 0, cols - 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            path.append((top, col))
        top += 1

        for row in range(top, bottom + 1):
            path.append((row, right))
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                path.append((bottom, col))
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                path.append((row, left))
            left += 1

    return path

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
		path = make_spiral_path(8, 10)
		enemy_count = data["remaining_enemies"]

		self._rounds = [
			RoundConfig(
				enemies=[lambda p: RegeneratorChameleonUbe(p) for _ in range(enemy_count)],
				path=path,
				player_start=(4, 5),
			),
			RoundConfig(
				enemies=[lambda p: RegeneratorChameleonUbe(p) for _ in range(enemy_count + 2)],
				path=path,
				player_start=(4, 5),
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
			enemies=[lambda p: RegeneratorChameleonUbe(p) for _ in range(count)],
			path=self._path,
			player_start=(5, 5),
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
	
		