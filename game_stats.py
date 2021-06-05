import json
class GameStats:
	"""track the statistics for the game"""
	def __init__(self,game):
		"""initialize the statistics"""
		self.settings=game.settings
		self.high_score=self.get_saved_high_score()
		self.reset_stats()
		# Start Alien Invasion in an inactive state.
		self.game_active=False


	def get_saved_high_score(self):
		"""get the high score from the file if it exists"""
		try:
			file_name='high_score.json'
			with open(file_name) as file_object:
				return json.load(file_object)
		except FileNotFoundError:
			return 0

	def reset_stats(self):
		"""initialize the statistics that change during the game"""
		self.ships_left=self.settings.ship_limit
		self.score=0
		self.level=1