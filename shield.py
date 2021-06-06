from pygame.sprite import Sprite
import pygame

class Shield(Sprite):
	"""shield for the ship"""
	def __init__(self,game):
		"""initialize the attributes for the shield"""
		super().__init__()
		self.screen=game.screen
		self.settings=game.settings
		self.screen_rect=self.screen.get_rect()
		#shield properties.
		self.image=pygame.image.load("images/shield.bmp")
		self.rect=self.image.get_rect()

