from alien_invasion import AlienInvasion
import pygame
from random import random

class AIPlayer:
    """Automatic player for Alien Invasion."""
    def __init__(self,game):
        """initialize the attributes of the ai player"""
        self.game=game
        self.settings=game.settings


    def run_game(self):
        """run the automated game"""
        #start out the game in an active state and hide the mouse.
        self.game.stats.game_active=True
        pygame.mouse.set_visible(False)
        #how fast the game is played.self.
        self._modify_speed(1)
        self.fleet_size=len(self.game.aliens.sprites())
        self.game.ship.moving_right=True
        while True:
            self.game._check_events()
            if self.game.stats.game_active:
                self.game._update_bullets()
                self.game._update_aliens()
                self._strategy()
                self._fire_bullets()
                self._ship_update()
            self.game._update_screen()

    def _strategy(self):
        """implement the strategy"""
        if len(self.game.aliens.sprites())<0.5*self.fleet_size:
            self._target_aliens()


    def _target_aliens(self):
        """kill specific aliens"""
        target_alien=self._get_target_alien()
        ship=self.game.ship
        if (ship.rect.x > target_alien.rect.x-15 
            and self.settings.fleet_direction==-1):
            ship.moving_right=False
        elif (ship.rect.x<target_alien.rect.x+15
            and self.settings.fleet_direction==1):
            ship.moving_right=True

    def _get_target_alien(self):
        """return the target alien"""
        target_alien=self.game.aliens.sprites()[0]
        for alien in self.game.aliens.sprites():
            if alien.rect.y > target_alien.rect.y:
                target_alien=alien
            elif alien.rect.x > target_alien.rect.x:
                target_alien=alien
        return target_alien
        

    def _fire_bullets(self):
        """fire bullets"""
        #how frequent should the ship fire bullets 
        #when there are only 7 aliens left.
        firing_frequency=1.007
        if len(self.game.aliens.sprites()) < 7:
            if random()<firing_frequency:
                self.game._fire_bullet()
        else:
            self.game._fire_bullet()


    def _ship_update(self):
        """move the ship continuously to the right and left"""
        ship=self.game.ship
        if ship.rect.right<self.game.screen.get_rect().right and ship.moving_right:
            ship.x+=self.settings.ship_speed
        else:
            ship.moving_right=False
            if ship.rect.left>0:
                ship.x-=self.settings.ship_speed
            else:
                ship.moving_right=True
        ship.rect.x=ship.x

    def _modify_speed(self,speed_factor):
        """modify the speed of the game"""
        self.settings.ship_speed*=speed_factor
        self.settings.bullet_speed*=speed_factor
        self.settings.alien_speed*=speed_factor



if __name__=='__main__':
    game=AlienInvasion()
    ai_game=AIPlayer(game)
    ai_game.run_game()
