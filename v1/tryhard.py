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

			# Split by N
			split_hist = game.historystr.split('N')
			
			# Do all of this for preflop
			if len(split_hist) == 1:
				h = split_hist[0]
				# Simple actions
				if re.search('k',h) != None:
					moveseat = re.search('k',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'CHECK'

				if re.search('c',h) != None:
					moveseat = re.search('c',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'CALL'

				if re.search('r',h) != None:
					moveseat = re.search('r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'RAISE'

				# Complex actions
				if re.search('ppf',h) != None:
					moveseat = re.search('ppf',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'BTN_FOLD'

				if re.search('ppc',h) != None:
					moveseat = re.search('ppc',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'BTN_CALL'

				if re.search('ppr',h) != None:
					moveseat = re.search('ppr',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'BTN_RAISE'

				if re.search('r.?r',h) != None:
					moveseat = re.search('r.?r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = '3_BET'
				
				if re.search('r.?r.?f',h) != None:
					moveseat = re.search('r.?r.?f',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'F_3_BET'

				if re.search('r.?r.?r',h) != None:
					moveseat = re.search('r.?r.?r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = '4_BET'
				
				if re.search('r.?r.?r.?f',h) != None:
					moveseat = re.search('r.?r.?r.?f',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'F_4_BET'

				if re.search('r.?r.?r.?r',h) != None:
					moveseat = re.search('r.?r.?r.?r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = '5_BET'
				
				if re.search('r.?r.?r.?r.?f',h) != None:
					moveseat = re.search('ppf',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'F_5_BET'

			if len(split_hist) >= 2:
				h = split_hist[-1]
				# Simple actions
				if re.search('k',h) != None:
					moveseat = re.search('k',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'CHECK'

				if re.search('c',h) != None:
					moveseat = re.search('c',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'CALL'

				if re.search('r',h) != None:
					moveseat = re.search('r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'RAISE'

				# Complex actions
				if re.search('r{1}',h[:2]) != None:
					moveseat = re.search('r{1}',h[:2]).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'DONK_BET'

				if re.search('(r{1}).?f',h[:2]) != None:
					moveseat = re.search('(r{1}).?f',h[:2]).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'F_DONK_BET'

				if re.search('(kr)|(k-r)|(kkr)',h[:3]) != None:
					moveseat = re.search('(kr)|(k-r)|(kkr)',h[:3]).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'C_BET'

				if re.search('((kr)|(k-r)|(kkr)).?f',h[:3]) != None:
					moveseat = re.search('((kr)|(k-r)|(kkr)).?f',h[:3]).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = 'F_C_BET'

				if re.search('r.?r',h) != None:
					moveseat = re.search('r.?r',h).end() % 3
					moveind = g.ind2seat[moveseat]
					g.p[moveind].last_move = '2_RAISE'






			for vil in g.p[1:]:
				vil.last_move = 'RAISE'

		@staticmethod
	   	def retrospect(game,historypak):
	   		pass
