import pygame.font
from pygame.sprite import Group
from ship import Ship
import pygame

class Scoreboard:
    """the scoreboard of the game"""
    def __init__(self,game):
        """initialize the attributes of the scoreboard"""
        self.settings=game.settings
        self.game=game
        self.screen=game.screen
        self.screen_rect=self.screen.get_rect()
        self.stats=game.stats
        #properties.
        self.font=pygame.font.SysFont(None,48)
        self.text_color=(50,50,50)
        self.high_score_sound=pygame.mixer.Sound("sounds/high_score.ogg")
        self.high_score_sound1=True
        self.prep_images()
        

    def prep_images(self):
        """prepare images"""
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        """prepare the score"""
        rounded_score=round(self.stats.score,-1)
        score="{:,}".format(rounded_score)
        self.img=self.font.render(
            score,True,self.text_color,self.settings.bg_color)
        self.img_rect=self.img.get_rect()
        self.img_rect.right=self.screen_rect.right - 20
        self.img_rect.top=20

    def prep_high_score(self):
        """prepare the high score"""
        #prepare the high_score by rounding it 
        #and putting it in the right format.
        rounded_score=round(self.stats.high_score,-1)
        score="{:,}".format(rounded_score)
        #make it as an image.
        self.img2=self.font.render(
            score,True,self.text_color,self.settings.bg_color)
        #get its rect.
        self.img2_rect=self.img2.get_rect()
        #set its position.
        self.img2_rect.centerx=self.screen_rect.centerx
        self.img2_rect.top=self.img_rect.top


    def check_high_score(self):
        """check to see if there is a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score=self.stats.score
            self.prep_high_score()
            if self.high_score_sound1:
                self.high_score_sound.play()
                self.high_score_sound1=False

    def prep_level(self):
        """prepare the level number"""
        level_str=str(self.stats.level)
        self.lvl_img=self.font.render(
            level_str,True,self.text_color,self.settings.bg_color)
        #set the position.
        self.lvl_img_rect=self.lvl_img.get_rect()
        self.lvl_img_rect.right=self.img_rect.right
        self.lvl_img_rect.top=self.img_rect.bottom + 10


    def prep_ships(self):
        """Show how many ships are left."""
        self.ships=Group()
        for ship_number in range(self.stats.ships_left):
            ship=Ship(self.game)
            ship.rect.x=10+ship_number*ship.rect.width
            ship.rect.y=10
            self.ships.add(ship)


    def draw_score(self):
        """draw the scores,the level and the ships to the screen"""
        self.screen.blit(self.img,self.img_rect)
        self.screen.blit(self.img2,self.img2_rect)
        self.screen.blit(self.lvl_img,self.lvl_img_rect)
        self.ships.draw(self.screen)
