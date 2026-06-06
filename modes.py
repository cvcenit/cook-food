from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from entities.enemies import Ube, Chameleon, Regenerator, Kutsinta, Gulaman, Palitaw, Lecheflan, Champorado
from entities.towers import Tower
from grid import Grid
from random import choice


@dataclass
class RoundConfig:
	enemies: list # list of callables
	paths: list
	player_start: tuple
	grid: Grid # added grid in round config
	tunnels: list[tuple[int, int]] = None

# WILL PROBABLY NOT BE USED BUT WILL LEAVE HERE
def make_spiral_path(rows=8, cols=10, row_offset=1):
    path = []
    top, bottom, left, right = 0, rows - 1, 0, cols - 1

    while top <= bottom and left <= right:
        for col in range(left, right + 1):
            path.append((top + row_offset, col))
        top += 1

        for row in range(top, bottom + 1):
            path.append((row + row_offset, right))
        right -= 1

        if top <= bottom:
            for col in range(right, left - 1, -1):
                path.append((bottom + row_offset, col))
            bottom -= 1

        if left <= right:
            for row in range(bottom, top - 1, -1):
                path.append((row + row_offset, left))
            left += 1

    return path

class Level(ABC):
	#@abstractmethod
	#def get_round(self, index: int) -> RoundConfig:
	#	...
	
	@property
	@abstractmethod
	def initial_lives(self) -> int:
		...

	@property
	@abstractmethod
	def initial_exp(self) -> int:
		...

class CampaignMode(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		path1 = [
			(1, 0), (1, 1), (1, 2), (1, 3), (1, 4), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (1, 10),
			(2, 10), (3, 10), (4, 10), (5, 10), (6, 10), (7, 10),
			(7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4), (7, 3), (7, 2), (7, 1),
			(6, 1), (5, 1), (4, 1), (3, 1),
			(3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (3, 8),
			(4, 8), (5, 8),
			(5, 7), (5, 6), (5, 5),
			]
		
		path2 = []
		
		tunnels = []
		
		tiles = list(set(path1 + path2))
		grid = Grid(9, 11, tiles, tunnels)
		enemy_count = data["remaining_enemies"]

		valid_paths = [p for p in [path1, path2] if p]
		self._rounds = [
			RoundConfig(
				enemies=[(lambda p, cls=Ube: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Kutsinta: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Gulaman: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Palitaw: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Lecheflan: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Champorado: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
		]
		self._initial_lives = data["remaining_lives"]
		self._available_towers = available_towers
	
	@property
	def rounds(self) -> list[RoundConfig]:
		return self._rounds
	
	@property
	def initial_lives(self) -> int:
		return self._initial_lives
	
	@property
	def initial_exp(self) -> int:
		return 0

	@property
	def available_towers(self):
		return self._available_towers

	def get_round(self, index: int) -> RoundConfig:
		return self._rounds[index]

class Level1(CampaignMode):
	def __init__(self, data: dict, available_towers: list[Tower]):
			super().__init__(data, available_towers)

class Level2(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		path1 = [
			(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), # goes down
			(6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9), # goes right
			(5, 9), (4, 9), (3, 9), (2, 9), # goes up
			(2, 8), (2, 7), (2, 6), (2, 5), # goes left
			(3, 5), # goes down
			(3, 4), (3, 3), # goes left 
			(2, 3), (1, 3) # goes up
			]
		
		path2 = []
		
		tunnels = []
		
		tiles = list(set(path1 + path2))
		grid = Grid(9, 11, tiles, tunnels)
		enemy_count = data["remaining_enemies"]
		self._available_towers = available_towers

		valid_paths = [p for p in [path1, path2] if p]
		self._rounds = [
			RoundConfig(
				enemies=[(lambda p, cls=Ube: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Kutsinta: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Gulaman: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Palitaw: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Lecheflan: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Champorado: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
		]
		self._initial_lives = data["remaining_lives"]

	@property
	def rounds(self):
		return self._rounds
	
	@property
	def initial_lives(self):
		return self._initial_lives
	
	@property
	def initial_exp(self):
		return 0
	
	@property
	def available_towers(self):
		return self._available_towers
	
	def get_round(self, index):
		return self._rounds[index]
	
class Level3(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		path1 = [
			(4, 0), (4, 1),
			(3, 1), (2, 1),
			(2, 2), (2, 3),
			(3, 3), (4, 3), (5, 3), (6, 3),
			(6, 4), (6, 5), (6, 6), (6, 7),
			(5, 7), (4, 7), (3, 7), (2, 7),
			(2, 8), (2, 9),
			(3, 9), (4, 9),
			(4, 10)
			]
		
		path2 = []
		
		tunnels = []
		
		tiles = list(set(path1 + path2))
		grid = Grid(9, 11, tiles, tunnels)
		enemy_count = data["remaining_enemies"]
		self._available_towers = available_towers

		valid_paths = [p for p in [path1, path2] if p]
		self._rounds = [
			RoundConfig(
				enemies=[(lambda p, cls=Ube: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Kutsinta: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Gulaman: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Palitaw: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Lecheflan: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Champorado: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
		]
		self._initial_lives = data["remaining_lives"]

	@property
	def rounds(self):
		return self._rounds
	
	@property
	def initial_lives(self):
		return self._initial_lives
	
	@property
	def initial_exp(self):
		return 0
	
	@property
	def available_towers(self):
		return self._available_towers
	
	def get_round(self, index):
		return self._rounds[index]

class Level4(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		path1 = [
			(6, 10), (6, 9),
			(5, 9), (4, 9),
			(4, 8), (4, 7),
			(3, 7), (2, 7),
			(2, 6), (2, 5), (2, 4), (2, 3),
			(3, 3), (4, 3),
			(4, 2), (4, 1),
			(3, 1), (2, 1),
			(2, 0),
			]
		
		path2 = [
			(6, 0), (6, 1),
			(5, 1), (4, 1),
			(4, 2), (4, 3),
			(5, 3), (6, 3),
			(6, 4), (6, 5), (6, 6), (6, 7),
			(5, 7), (4, 7),
			(4, 8), (4, 9),
			(3, 9), (2, 9),
			(2, 10),
		]
		
		tunnels = []
		
		tiles = list(set(path1 + path2))
		grid = Grid(9, 11, tiles, tunnels)
		enemy_count = data["remaining_enemies"]
		self._available_towers = available_towers

		valid_paths = [p for p in [path1, path2] if p]
		self._rounds = [
			RoundConfig(
				enemies=[(lambda p, cls=Ube: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Kutsinta: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Gulaman: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Palitaw: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Lecheflan: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Champorado: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
		]
		self._initial_lives = data["remaining_lives"]

	@property
	def rounds(self):
		return self._rounds
	
	@property
	def initial_lives(self):
		return self._initial_lives
	
	@property
	def initial_exp(self):
		return 0
	
	@property
	def available_towers(self):
		return self._available_towers
	
	def get_round(self, index):
		return self._rounds[index]

class Level5(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		# HARDCODED PATH FOR THE USAGE OF COLORS IN MAP
		path1 = [
			(6, 0), (6, 1), (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7),
			(5, 7), (5, 8),
			(4, 8), (3, 8),
			(3, 7), (2, 7),
			(2, 6), (2, 5),
			(1, 5),
			]
		
		path2 = [
			(6, 10), (6, 9), (6, 8), (6, 7), (6, 6), (6, 5), (6, 4), (6, 3),
			(5, 3), (5, 2),
			(4, 2), (3, 2),
			(3, 3), (2, 3),
			(2, 4), (2, 5),
			(1, 5),
		]
		
		tunnels = []
		
		tiles = list(set(path1 + path2))
		grid = Grid(9, 11, tiles, tunnels)
		enemy_count = data["remaining_enemies"]
		self._available_towers = available_towers

		valid_paths = [p for p in [path1, path2] if p]
		self._rounds = [
			RoundConfig(
				enemies=[(lambda p, cls=Ube: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Kutsinta: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Gulaman: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Palitaw: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Lecheflan: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
			RoundConfig(
				enemies=[(lambda p, cls=Champorado: cls(p), choice(valid_paths)) for _ in range(enemy_count)],
				paths=valid_paths,
				player_start=(4, 5),
				grid=grid,
				tunnels=tunnels,
			),
		]
		self._initial_lives = data["remaining_lives"]

	@property
	def rounds(self):
		return self._rounds
	
	@property
	def initial_lives(self):
		return self._initial_lives
	
	@property
	def initial_exp(self):
		return 20
	
	@property
	def available_towers(self):
		return self._available_towers
	
	def get_round(self, index):
		return self._rounds[index]

class EndlessMode(Level):
	def __init__(self, data: dict, available_towers: list[Tower]):
		self._base_count = data["remaining_enemies"]
		self._initial_lives = data["remaining_lives"]
		self._path = [
            (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
            (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8), (6, 9),
            (5, 9), (4, 9), (3, 9), (2, 9),
            (2, 8), (2, 7), (2, 6), (2, 5),
            (3, 5), (3, 4), (3, 3),
            (2, 3), (1, 3)
			]
		tunnels = [(3, 1), (4, 1), (6, 4), (6, 5), (6, 6)]
		self._grid = Grid(9, 11, self._path, tunnels)
		self._tunnels = tunnels
		self._available_towers = available_towers
		
	def get_round(self, round_num: int) -> RoundConfig:
		enemies = self._generate_round_enemies(round_num)
		
		return RoundConfig(
			enemies=enemies,
			paths=[self._path],
			player_start=(4, 5),
			grid=self._grid,
			tunnels=self._tunnels
		)
	
	def _generate_round_enemies(self, round_num: int):
		enemy_types = [Ube, Kutsinta, Gulaman, Palitaw, Lecheflan, Champorado, Chameleon, Regenerator]
		# TODO: more special enemies for higher rounds

		count = 3 + round_num // 2  # 3, 3, 4, 4, 5, 5, 6, 6
		speed_multiplier = 1.0 + (0.25 * round_num)

		enemies = [
			(lambda p, cls=choice(enemy_types), spd=speed_multiplier: cls(p, speed_multiplier=spd), self._path)
			for _ in range(count)
		]

		return enemies

	@property
	def rounds(self) -> list[RoundConfig]:
		return []
	
	@property
	def initial_lives(self) -> int:
		return self._initial_lives

	@property
	def available_towers(self):
		return self._available_towers

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
	
		