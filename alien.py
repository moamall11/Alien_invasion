import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
	"""a class to manage the alien's assets and behavior"""
	def __init__(self,game):
		"""initialize the alien's attributes"""
		super().__init__()
		self.screen=game.screen
		#use the settings of the game.
		self.settings=game.settings
		#set the image and the rect of the alien.
		self.image=pygame.image.load("images/alien.bmp")
		self.rect=self.image.get_rect()
		#set the position of the alien to the top left of the screen.
		self.rect.x=self.rect.width
		self.rect.y=self.rect.height
		#store the alien's exact horizontal position.
		self.x=float(self.rect.x)


	def update(self):
		"""update the position of the alien"""
		self.x += (self.settings.alien_speed * self.settings.fleet_direction)
		self.rect.x = self.x


	def check_edges(self):
		"""return True when the alien reaches the edge of the screen"""
		self.screen_rect=self.screen.get_rect()
		if self.rect.right >= self.screen_rect.right or self.rect.left <= 0:
			return True
