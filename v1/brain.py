from game import *

class Brain:
	"""
	This collection of static methods is responsible for deciding the optimal 
	action given a game state. We first determine an pdf range of hole cards
	for each opponent based on their betting style and characteristics. We then
	use this pdf to determine optimal play.
	"""
	@staticmethod
	def play(game):
		"""
		The main function of brain: return the optimal action. This involves
		calling the analyze method and the decide method.
		"""
		pass

	@staticmethod
	def analyze(game):
		"""
		Update the villain traits and pdfs based on recent moves (phase 1).
		"""
		pass

	@staticmethod
	def decide(game): #We may not need history here
		"""
		Determine the best course of action given the villain pdfs (phase 2).
		"""
		pass

	@staticmethod
	def retrospect(game):
		"""
		Update only the villain traits (not the pdfs) based on recent moves and
		the showdown at the end of a hand.
		"""
		pass
