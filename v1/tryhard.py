class Tryhard:
	"""
	This class handles looking over all the previous actions in a hand 
	to identify special moves (like 3-bets).
	"""

	@staticmethod
	def study(game,historypak):
		"""
		Updates game move history given a historypak.
		Also determine whether a player has folded.
		"""
		g = game # For easy typing
		g.history = map(lambda s: s.split(':'),historypak)


		for m in g.history:

			# Check if current player has folded
			if not g.p[g.seat2ind[g.action_on]].isIn:
				print g.p[g.seat2ind[g.action_on]].name + ' has folded- skipping.'
				g.historystr += '-' # Skip player
				g.action_on = (g.action_on+1) % 3

			if m[0] == 'POST':
				g.historystr += 'p'
				g.action_on = (g.action_on+1) % 3
			elif m[0] == 'RAISE' or m[0] == 'BET':
				g.historystr += 'r'
				g.action_on = (g.action_on+1) % 3
			elif m[0] == 'CALL':
				g.historystr += 'c'
				g.action_on = (g.action_on+1) % 3
			elif m[0] == 'CHECK':
				g.historystr += 'k'
				g.action_on = (g.action_on+1) % 3
			elif m[0] == 'FOLD':
				g.historystr += 'f'
				g.p[g.seat2ind[g.action_on]].isIn = False
				g.action_on = (g.action_on+1) % 3
			else: # New cards
				g.historystr += 'N'
				g.action_on = 1 # Set back to SB

		print 'HAND:		  ' + str(g.hands_idx)
		print 'HISTORY:	      ' + str(g.history)
		print 'HISTORYSTR:	  ' + g.historystr

		@staticmethod
		def assimilate(game):
			"""
			Looks at the previous game moves and identifies advanced poker
			techniques.
			"""
			# TODO: Use regex rules here on game.historystr
			# For now, just return RAISE

			for vil in g.p[1:]:
				vil.last_move = 'RAISE'

		@staticmethod
	   	def retrospect(game,historypak):
	   		pass
