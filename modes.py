from abc import ABC, abstractmethod


class GameMode(ABC):
	pass

class EndlessMode(GameMode):
	pass

class CampaignMode(GameMode):
	pass

class Level(ABC):
	# consists of a grid, with a path (?)
	pass


class GameOverCondition(ABC):
	@abstractmethod
	def is_game_over(self):
		pass

class RoundOverCondition(ABC):
	@abstractmethod
	def is_round_over(self):
		pass

class CampaignModeGameOverCondition(GameOverCondition):
	def __init__(self):
		self._is_game_over = False

	def is_game_over(self, enemies: int, lives: int, rounds: int):
		if (enemies <= 0 and rounds <= 0) or lives <= 0:
			self._is_game_over = True
		
		return self._is_game_over


class NoEnemiesRoundOverCondition(RoundOverCondition):
	def __init__(self):
		self._is_round_over = False

	def is_round_over(self, enemies: int):
		if enemies <= 0:
			self._is_round_over = True
		return self._is_round_over
	
		