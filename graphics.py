from abc import ABC, abstractmethod
import pyxel


class Button(ABC):
	@abstractmethod
	def is_clicked(self) -> bool:
		...

	@abstractmethod
	def is_hovered(self) -> bool:
		...
	

class TextButton(Button):
	def __init__(self, view):
		img = pyxel.Image.text(0, 0, "HELLO", 0, font=None)

	def is_clicked(self):
		...

class SpriteButton(Button):
	pass

class Screen:
	# Will have its own model, view, controller
	# its only methods are update and draw, which is also the update of the controller, and the draw of the view
	pass

class GridLayout:
	# ang demanding
	pass