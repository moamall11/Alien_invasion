import pygame.font

class Button2:
	"""the button object of the game"""
	def __init__(self,game,msg):
		"""initialize the attributes of the button"""
		self.screen=game.screen
		self.screen_rect=self.screen.get_rect()
		#set the properties and the dimensions of the button.
		self.width,self.height=200,50
		self.button_color=(110,150,0)
		self.text_color=(255,255,255)
		self.font=pygame.font.SysFont(None,48)

		#build the button's rect object and set it to the center of the screen.
		self.rect=pygame.Rect(0,0,self.width,self.height)
		self.rect.center=self.screen_rect.center
		self.rect.y+=110

		#prepare the message of the button only once.
		self._prep_msg(msg)


	def _prep_msg(self,msg):
		"""Turn msg into a rendered image and center text on the button."""
		#make the image of the text.
		self.msg_image=self.font.render(
			msg,True,self.text_color,self.button_color)
		#find the rect of that image.
		self.msg_rect=self.msg_image.get_rect()
		#set the position of the text.
		self.msg_rect.center=self.rect.center


	def draw_button(self):
		"""Draw blank button and then draw message."""
		self.screen.fill(self.button_color,self.rect)
		self.screen.blit(self.msg_image,self.msg_rect)