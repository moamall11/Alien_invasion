#this is a game about a space-ship that fires bullets at aliens
#let's import the required modules for the game
import sys
from time import sleep
import pygame
from settings import Settings
from ship import Ship
from game_stats import GameStats
from bullet2 import Bullet2
from bullet import Bullet
from alien import Alien
from button import Button
from random import random
from shield import Shield

#let's make a class of the game
class AlienInvasion:
    """Overall class to manage game assets and behavior."""
    def __init__(self):
        """initialize the game's attributes"""
        pygame.init()
        #make an instance of settings so that we can use it elsewhere
        self.settings=Settings()
        #set the width and height of the window
        self.screen=pygame.display.set_mode(
            (self.settings.screen_width,self.settings.screen_height),
            #pygame.RESIZABLE
            #(0,0),pygame.FULLSCREEN
            )
        #self.settings.screen_width = self.screen.get_rect().width
        #self.settings.screen_height = self.screen.get_rect().height
            
        #set the caption of the window
        pygame.display.set_caption("Alien Invasion")
        # Create an instance to store game statistics.
        self.stats=GameStats(self)
        self.ship=Ship(self)
        self.bullets=pygame.sprite.Group()
        self.bullets2=pygame.sprite.Group()
        self.aliens=pygame.sprite.Group()
        self._create_fleet()
        #make the play button.
        self.play_button=Button(self,"Play")
        self.num=0
        self.shields=pygame.sprite.Group()
        self._create_shields()


    def run_game(self):
        """the main loop of the game"""
        while True:
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_shields()
                self._update_aliens()
            self._update_screen()


    def _check_events(self):
        """loop through the events that happen by the user in the game"""
        for event in pygame.event.get():
            #when the user clicks the close button exit the game.
            if event.type == pygame.QUIT:
                sys.exit()
            #detect the event when the user presses a key.
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            #detect the event when the user releases a key.
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            #detect the event when the user presses the mouse button.
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos=pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)


    def _check_play_button(self,mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked=self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self._start_game()

    def _start_game(self):
        """start the game"""
        #reset the game statistics and activate the game.
        self.stats.reset_stats()
        self.stats.game_active=True
        #clear any existing aliens and bullets.
        self.aliens.empty()
        self.bullets.empty()
        self.bullets2.empty()
        #create a new fleet of aliens and center the ship.
        self._create_fleet()
        self.ship.center_ship()
        #hide the mouse's curser.
        pygame.mouse.set_visible(False)
        #reset the speed of the game.
        self.settings.initialize_dynamic_settings()
        self._create_shields()

    def _check_keydown_events(self,event):
        """respond to the keys pressed by the user"""
        #when the user presses the right arrow key 
        #set the moving_right flag to True
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=True
        #when the user presses the left arrow key
        #set the moving_left flag to True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=True
        #exit the game when the user presses 'q'
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_p:
            self._start_game()
            

    def _check_keyup_events(self,event):
        """respond to the keys released by the user"""
        #when the user releases the right arrow key
        #set the moving_right flag to False.
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right=False
        #when the user releases the left arrow key
        #set the moving_left flag to False.
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left=False
        #fire a bullet when the user presses the spacebar.
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _update_bullets(self):
        """update the positions of bullets 
        and removed the disappeared bullets"""
        self.bullets.update()
        self.bullets2.update()
        #get rid of the bullets that have disappeared f=rom the screen.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        for bullet in self.bullets2.copy():
            if bullet.rect.bottom >= self.settings.screen_height:
                self.bullets2.remove(bullet)
        self._check_bullet_alien_collisions()
        

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        #Remove any bullets and aliens that have collided.
        collisions=pygame.sprite.groupcollide(
            self.bullets,self.aliens,True,True)
        
        if not self.aliens.sprites():
            #when the user destroies all the aliens 
            #delete the existing bullets and make a new fleet of aliens.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()
            self.num+=1


    def _fire_bullet(self):
        """add a new bullet to the group of fired bullets"""
        if len(self.bullets) < self.settings.bullet_limit:
            new_bullet=Bullet(self)
            #add a new instance to the group of bullets 
            #unless the group already reached the limit of allowed bullets.
            self.bullets.add(new_bullet)

    def _create_fleet(self):
        """create a fleet of aliens"""
        #create an instance of alien to get it's width.
        alien=Alien(self)
        #calculate it's width and height to see how many aliens 
        #can fit the screen horizontally and vertically.
        alien_width,alien_height=alien.rect.size
        ship_height=self.ship.rect.height
        #calculating the available space by subtracting 
        #two alien's width from the width of the screen.
        available_space_x=self.settings.screen_width - (2 * alien_width)
        #same way when calculating the vertical space.
        available_space_y = (self.settings.screen_height - 
        (3 * alien_height) - ship_height)
        #then using floor division to divide the available space
        #so we can have a space between the aliens equal to one alien's width.
        number_aliens_x = available_space_x // (2 * alien_width)
        #same way to calculate the number of rows.
        number_rows = available_space_y // (2 * alien_height)
        #now we can make the fleet of aliens.
        for number_row in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,number_row)


    def _create_alien(self,alien_number,number_row):
        """create a new alien and add it to the fleet"""
        #make a new alien.
        alien=Alien(self)
        #get its width.
        alien_width,alien_height=alien.rect.size
        #calculate its decimal rect.
        alien.x=alien_width + 2 * alien_width * alien_number
        #return the value of the rect.
        alien.rect.x = alien.x
        alien.rect.y=alien_height + 2*alien_height*number_row
        #add the alien to the fleet.
        self.aliens.add(alien)

    def _update_shields(self):
        """update the number of shields"""
        collisions2=pygame.sprite.spritecollideany(self.ship,self.bullets2)
        if collisions2:
            for bullet in self.bullets2.copy():
                self.bullets2.remove(bullet)
                break
            for shield in self.shields.copy():
                self.shields.remove(shield)
                break
        if not self.shields.sprites():
            self._ship_hit()


    def _update_aliens(self):
        """update the positions of the fleet of aliens 
        after checking if the fleet hit an edge"""
        self._check_fleet_edges()
        self.aliens.update()
        #check for alien-ship collisions.
        if pygame.sprite.spritecollideany(self.ship,self.aliens):
            self._ship_hit()
        #check if an alien reaches the bottom of the screen.
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """check to see if the fleet hits the edge of the screen"""
        for alien in self.aliens.sprites():
            if random() < self.settings.bullet_frequency:
                
                new_bullet=Bullet2(self)
                self.bullets2.add(new_bullet)
                new_bullet.rect.x=alien.rect.x
                new_bullet.y=alien.rect.y
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """drop down the feet and then change the direction of the fleet"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """respond when the ship gets hit by an alien"""
        if self.stats.ships_left > 0:
            #decrement the number of ships left by 1.
            self.stats.ships_left-=1
            #delete the current aliens and bullets.
            self.aliens.empty()
            self.bullets.empty()# Create an instance to store game statistics.
            #center the ship.
            self.ship.center_ship()
            #create a new fleet of aliens.
            self._create_fleet()
            self._create_shields()
            #pause.
            sleep(0.5)
        else:
            self.stats.game_active=False
            #show the mouse curser.
            pygame.mouse.set_visible(True)
            print(self.num)

    def _check_aliens_bottom(self):
        """respond if any alien has reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.screen.get_rect().bottom:
                #when an alien reaches the bottom of the screen
                #respond the same way as if the ship was hit by an alien.
                self._ship_hit()
                break

    def _create_shields(self):
        """create shields"""
        for shield_number in range(self.settings.shields_limit):
            shield=Shield(self)
            shield.rect.y+=10
            shield.rect.left=self.settings.screen_width-60 - (
                shield_number*shield.rect.width)
            self.shields.add(shield)


    def _update_screen(self):
        """update the images on the screen and flip to the new screen"""
        #fill the surface of the screen with the background color.
        self.screen.fill(self.settings.bg_color)
        #draw the ship to the screen.
        self.ship.blitme()
        #draw the bullets to the screen.
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for bullet in self.bullets2.sprites():
            bullet.draw_bullet()
        #draw the aliens to the screen.
        self.aliens.draw(self.screen)
        #draw the play button when the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()
        self.shields.draw(self.screen)
        #draw to the screen the last made screen.
        pygame.display.flip()


#create an instance of the game and run 'run_game'
if __name__=='__main__':
    game=AlienInvasion()
    game.run_game()
