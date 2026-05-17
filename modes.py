from collections.abc import ABC, abstractmethod


class GameMode(ABC):
	pass

class EndlessMode(GameMode):
	pass

class CampaignMode(GameMode):
	pass

class GameOverCondition(ABC):
	@abstractmethod
	def is_game_over(self):
		pass

class RoundOverCondition(ABC):
	@abstractmethod
	def is_round_over(self):
		pass

class Level(ABC):
	# consists of a grid, with a path (?)
	pass


class SimpleGameOverCondition(GameOverCondition):
	def __init__(self, enemies: int, lives: int, round: int):
		self._enemies = enemies
		self._lives = lives
		self._round = round
		self._is_game_over = False

	def is_game_over(self):
		return self._is_game_over
	
	def check_all_enemies_gone_at_last_round(self):
		if self._enemies <= 0 and round == 0:
			self._is_game_over = True

	def check_game_over(self):
		if self._lives <= 0:
			self._is_game_over = True


class SimpleRoundOverCondition(RoundOverCondition):
	def __init__(self, enemies: int):
		self._enemies = enemies
		self._is_round_over = False

	def is_round_over(self):
		return self._is_round_over
	
	def check_all_enemies_gone(self):
		if self._enemies <= 0:
			self._is_round_over = True
		