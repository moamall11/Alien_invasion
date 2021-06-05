import pygame
from pygame.sprite import Sprite

class Ship(Sprite):
    """a class to manage the ship of Alien Invasion"""
    def __init__(self,game):
        """initialize the attributes for the ship and its starting position"""
        super().__init__()
        #let's identify the screen's surface and its rect.
        self.screen=game.screen
        self.screen_rect=game.screen.get_rect()
        #let's identify the ship's surface and it's rect.
        self.image=pygame.image.load('images/ship.bmp')
        self.rect=self.image.get_rect()
        #let's identify the initial position of the ship's surface on the screen
        self.rect.midbottom=self.screen_rect.midbottom
        #add the settingsvement flags."""
        self.settings=game.settings
        #convert the ship's x value to a decimal value
        self.x=float(self.rect.x)
        #movement flags
        self.moving_right=False
        self.moving_left=False


    def blitme(self):
        """draw the ship at its specified location"""
        self.screen.blit(self.image,self.rect)


    def center_ship(self):
        """put the ship in the center of the bottom of the screen"""
        self.rect.midbottom=self.screen_rect.midbottom
        self.x=float(self.rect.x)


    def update(self):
        """Update the ship's position based on the movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            #move the ship to the right
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            #move the ship to the left
            self.x -= self.settings.ship_speed
        #return the decimal value to the x value of the ship
        self.rect.x = self.x