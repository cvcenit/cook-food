from collections.abc import ABC


class Enemy(ABC):
	def __init__(self):
		self.hit_points = 20

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