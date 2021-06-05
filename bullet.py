import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """a class to manage the bullets fired from the ship"""
    def __init__(self,game):
        """initialize the attributes of the bullet"""
        #initialize the attributes of the parent class.
        super().__init__()
        #initilize the screen attribute from the game.
        self.screen=game.screen
        #initialize the settings from the game.
        self.settings=game.settings
        #set the color of the bullet from the settings.
        self.color=self.settings.bullet_color
        #create the bullet from scratch at (0,0).
        self.rect=pygame.Rect(0,0,self.settings.bullet_width,
            self.settings.bullet_height)
        #set the position of the bullet 
        #which will depend on the position of the ship. 
        self.rect.midtop=game.ship.rect.midtop
        #store the bullet's position as a decimal to ba able to
        #make a fine adjustment of the speed of the bullet.
        self.y=float(self.rect.y)

    def update(self):
        """update the position of the bullet"""
        #update the decimal position of the bullet.
        self.y -= self.settings.bullet_speed

        #update the rect value of the bullet.
        self.rect.y = self.y

    def draw_bullet(self):
        """draw the bullet to the screen"""
        #draw the rect with the specified color to the screen.
        pygame.draw.rect(self.screen,self.color,self.rect)
