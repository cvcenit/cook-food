from abc import ABC, abstractmethod


class GameMode(ABC):
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