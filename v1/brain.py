import math
import itertools as it
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
		Brain.analyze(game)
		return Brain.decide(game)

	@staticmethod
	def analyze(game):
		"""
		Update the villain traits and pdfs based on recent moves (phase 1).
		"""
		# Determine the equity curve based on the community cards
		g = game # For easy typing
		for v in g.p[1:]: # For each villain
			# Make sure villain hasn't folded and has made at least 1 move
			if v.isIn and v.last_move != '':
				'''
				# Grab the equity curve from the lookup table if not river
				if len(g.comm) != 5:
					# TBD: Make and use lookup table
					# v.equ = ...
				else:
					# TBD: Run Enumeration (45 choose 3 = 14190)
					# v.equ = ...
				'''
				print 'Running <analyze> on ' + v.name
				# Compute the action pdf given hole cards using cutoffs
				# Parameter determining betting variance (flakiness)
				sharp = 3 # Goes from 0 (flaky) to 10 (sharp)
				# low and high cut determine edges of cutoff
				[low_cut,high_cut] = v.cutoffs[v.last_move]
				# A shifted 2-term logistic converts equity to action pdf
				k = math.exp(sharp*0.5) # k parameter in logistic
				# The 0.05 offset is for edge cases
				logi = lambda x: ((1./(1+math.exp(-k*(x-low_cut+.05))))*
					(1./(1+math.exp(-k*(-x+high_cut+.05)))))
				# Apply the function
				v.act = map(logi,v.equ)
				# Normalize
				v.act = map(lambda x: x/float(sum(v.act)),v.act)

				# Use bayesian inference to determine v.pdf
				v.pdf = [a*b for a,b in it.izip(v.pdf,v.act)] # Can we use numpy here please?
				# Normalize
				v.pdf = map(lambda x: x/float(sum(v.pdf)),v.pdf)

				# TBD: Generate alias table for monte carlo sampling
				# TBD: Update villain traits?

	@staticmethod
	def decide(game):
		"""
		Determine the best course of action given the villain pdfs (phase 2).
		"""
		# Compute true equity using biased monte-carlo
		# true_equity = ...

		# Super simple bot: maxraise if equity >= .5 else checkfold

		# For now, just maxraise
		action = max(game.max_raise,game.call_amt)
		return action

	@staticmethod
	def retrospect(game):
		"""
		Update only the villain traits (not the pdfs) based on recent moves and
		the showdown at the end of a hand.
		"""
		pass
