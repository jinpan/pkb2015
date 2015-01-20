import re

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
		g = game
		# TODO: Use regex rules here on game.historystr

		# Split by N
		split_hist = game.historystr.split('N')
		
		# Do all of this for preflop
		if len(split_hist) == 1:
			h = split_hist[0]
			# Remove the H
			h = h[1:]
			# Simple actions
			for m in re.finditer('(?<=k)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'CHECK'

			for m in re.finditer('(?<=c)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'CALL'

			for m in re.finditer('(?<=r)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'RAISE'

			# Complex actions
			for m in re.finditer('(?<=(ppf))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_BTN'

			for m in re.finditer('(?<=(ppc))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'C_BTN'

			for m in re.finditer('(?<=(ppr))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'R_BTN'

			# Bets
			for m in re.finditer('(?<=(r.?r))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = '3_BET'

			for m in re.finditer('(?<=(r.?r.?f))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_3_BET'

			for m in re.finditer('(?<=(r.?r.?r))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = '4_BET'

			for m in re.finditer('(?<=(r.?r.?r.?f))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_4_BET'

			for m in re.finditer('(?<=(r.?r.?r.?r))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = '5_BET'

			for m in re.finditer('(?<=(r.?r.?r.?r.?f))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_5_BET'
		
		# Post flop
		if len(split_hist) >= 2:
			h = split_hist[-1]

			# Simple actions
			for m in re.finditer('(?<=k)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'CHECK'

			for m in re.finditer('(?<=c)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'CALL'

			for m in re.finditer('(?<=r)',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'RAISE'

			# Complex actions
			for m in re.finditer('(?<=(r{1}))',h[:2]):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'DONK_BET'

			for m in re.finditer('(?<=((r{1}).?f))',h[:2]):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_DONK_BET'

			for m in re.finditer('(?<=((kr)|(k-r)|(kkr)))',h[:3]):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'C_BET'

			for m in re.finditer('(?<=(((kr)|(k-r)|(kkr)).?f))',h[:3]):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = 'F_C_BET'

			for m in re.finditer('(?<=(r.?r))',h):
				moveind = g.seat2ind[m % 3]
				g.p[moveind].last_move = '2_RAISE'
			
		print [x.last_move for x in g.p]
	@staticmethod
   	def retrospect(game,historypak):
   		pass
