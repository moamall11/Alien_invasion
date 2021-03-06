class Settings:
    """A class to store all the settings for the Alien Invasion game."""
    def __init__(self):
        """initialize the game's static settings"""
        #screen settings
        self.screen_width=1200
        self.screen_height=650
        self.bg_color=(230,230,230)
        #ship settings
        self.ship_limit=3
        #bullet settings
        self.bullet_limit=3
        self.bullet_width=3
        self.bullet_height=15
        self.bullet_color=(60,60,60)
        self.alien_bullet_color=(255,0,0)
        #alien settings
        self.fleet_drop_speed=10
        self.bullet_frequency=0.0003
        #shield settings
        self.shields_limit=3
        # How quickly the game speeds up.
        self.speedup_scale=1.2
        #How quickly the alien points increase during the game.
        self.score_scale=1.5
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed=1.5
        self.bullet_speed=1.5
        #self.alien_speed=1
        self.alien_speed=0.6
        #scoring.
        self.alien_points=50
        #the direction 1 represent right and the direction -1 represent left.
        self.fleet_direction=1
       

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed*=self.speedup_scale
        self.bullet_speed*=self.speedup_scale
        self.alien_speed*=self.speedup_scale
        self.alien_points=int(self.alien_points*self.score_scale)

