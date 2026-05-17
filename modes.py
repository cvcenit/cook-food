from collections.abc import ABC, abstractmethod


class GameMode(ABC):
	@abstractmethod
	def end_condition(self):
		pass


class Player(ABC):
	@abstractmethod
	@property
	def lives(self):
		pass


class EndlessMode(GameMode):
	pass

class CampaignMode(GameMode):
	pass

class GameOverCondition(ABC):
	# different conditions sa campaign mode
	pass

class Level(ABC):
	# consists of a grid, with a path (?)
	pass