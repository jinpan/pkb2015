class Player:
	"""
	This class represents a player in poker. It has attributes but no methods.
	"""
	def __init__(self,name,stack):
		self.name = name
		self.stack = stack
		self.isActive = True # Whether busted or not
		self.seat = 1 # Default seat is button
		self.hole = [] # This should only be needed by the hero
		self.isin = True # Whether folded or not

class Villain(Player):
	"""
	This class represents a villain in poker. It has extra attributes which
	contains information on betting style etc. It may also have methods as part 
	of phase 1 of the brain.
	"""
	def __init__(self,name,stack):
		Player.__init__(self,name,stack)
		# TBD: Put villain traits here


		# Valid villain moves are currently: 
		# ['CHECKFOLD'], ['CALL',amt], ['RAISE',amt], ['NEWBET']
		# BET is included in RAISE and ENDBET is when new cards or streets open
		self.move_list = [['NEWBET']]

		# Note: 52 choose 2 = 1326
		self.pdf = [1/1326.]*1326 # PDF of hole cards
		self.cdf = map(lambda x: x/1326., xrange(1326)) # CDF of hole cards
		# Equity of hole cards (TBD: MAKE THIS THE UNIFORM PREFLOP EQUITY)
		self.equ = map(lambda x: x/1326., xrange(1326)) # Linear for now

		# Cutoffs are used to convert villain equity into villain pdfs.
		# Any equity >= the cutoff key will result in the key's move.
		self.cutoffs = { # Anything below CALL will be a CHECKFOLD
		'CALL': .5,
		'RAISE': .8
		}


class Game:
	"""
	This class represents a single round of Poker. As the round progresses and
   	more cards are put on the table, the Game object updates.
   	"""
   	def __init__(self, names,stack,bb,hands_max,timebank):
   		# Create list of players (of which we are index 0)
   		self.p = [Player(names[0],stack),Villain(names[1],stack),Villain(names[2],stack)]
   		self.names = names
   		self.seating = dict(zip([0,1,2],[0,1,2])) # Returns the seat given index
   		self.name2ind = dict(zip([x.name for x in self.p],[0,1,2])) # Returns index given name

   		# Set up the chips, table, & legal moves
   		self.pot = 0 # Pot size
   		self.comm = [] # List of community cards
   		self.bb = bb # Big blind value
   		self.legal = [] # List of legal moves
   		self.call_amt = 0 # Amount needed to call (if 0, hero can 'check')
   		self.min_raise = bb # Minimum raise
   		self.max_raise = bb+1 # Maximum raise
   		self.validRB = 'RAISE:' # Ignore this, just used to bet properly

   		# Set up the rest
   		self.timebank = timebank # Time left
   		self.hands_max = hands_max # Maximum number of hands engine will play
   		self.hands_idx = 1 # Current number of hands dealt
   		self.n_active = 3 # Number of currently active players (not busted)
   		self.legal = '' # Legal possible actions
